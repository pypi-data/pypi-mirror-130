//
// Created by jorge on 12/16/20.
//
#include "include/Dataset.h"
#include "MergerTask.h"
#include "MergerTasksList.h"
#include "SampleLocation.h"

#include <boost/log/core.hpp>
#include <boost/log/trivial.hpp>
#include <boost/log/expressions.hpp>
#include <boost/thread.hpp>

namespace logging = boost::log;


size_t
Dataset::getMetricNames(std::vector<std::string> & metrics) {
    if (chunkVector.size() > 0) {
        chunkVector[0]->getMetricNames(metrics);
        return metrics.size();
    }
    else {
        metrics = metricNames;
        return metricNames.size();
    }
}


void
Dataset::addChunk(Chunk *pChunk) {

    // Critical section
    mu.lock();
    this->chunkVector.emplace_back(pChunk);

    // total size of samplesInDataset
    samplesInDataset += pChunk->getSamplesCount();

    // Append metrics here.
    mu.unlock();
}


void
Dataset::addMergedMetric(std::string   metricName,  Dataset::MetricsPtr data) {

    // Critical section
    mu.lock();
    hashMapMetrics.emplace( metricName, data);
    // Append metrics here.
    mu.unlock();
}


void
Dataset::sortChunks() {
    struct {
        bool operator()(Chunk *a, Chunk *b) const { return a->getId() < b->getId(); }
    } compare;
    std::sort(chunkVector.begin(), chunkVector.end(), compare);
}


SampleLocation
Dataset::getLocationInChunks(uint64_t sample, bool fromStart)
{
    int chunkPos = Dataset::INVALID_CHUNK_NUMBER;
    int samplePos = Dataset::INVALID_TIMESTAMP_POS;

    // Easy cases
    if (sample == Dataset::INVALID_TIMESTAMP) {
        if (fromStart) { // first sample of first chunk
            chunkPos = 0;
            samplePos = 0;
        }
        else { // last sample of last chunk
            chunkPos = chunkVector.size()-1;
            samplePos =  ChunkMetric::MAX_SAMPLES-1;
        }

        return  SampleLocation(chunkPos,samplePos);
    }

    //
    int chunkNumber = 0;
    for (auto c: chunkVector) {
        if (sample >= c->getStart() && sample <= c->getEnd()) {  // this is the chunk
            chunkPos = chunkNumber;
            // Timestamps 'start' metrics are always the 0-th position
            auto ts = c->getMetric(0);
            for (int i = 0; i < ChunkMetric::MAX_SAMPLES; ++i) {
                if (ts->values[i] >= sample) {
                    samplePos = i;

                    if (i ==0 && !fromStart) {
                        // actually previous chunk
                        samplePos = ChunkMetric::MAX_SAMPLES - 1;
                        --chunkPos;
                    }
                    break;
                }
            }
            break;
        }
        ++chunkNumber;
    }
    SampleLocation pos(chunkPos,samplePos);
    return pos;
}


Dataset::MetricsPtr
Dataset::getMetric(std::string   metricName, uint64_t start, uint64_t end)
{
        auto start_chunk_pos = getLocationInChunks(start, true);
        auto end_chunk_pos = getLocationInChunks(end, false);

        // TODO:  in case of lazy parsing, we should be  parsing here
        if (this->LazyParsing)
            ; // for chunks between start and end, start parser threads

        Dataset::MetricsPtr p =  assembleMetricFromChunks(metricName, start_chunk_pos, end_chunk_pos);

        return p;
}


Dataset::MetricsPtr
Dataset::assembleMetricFromChunks(std::string metricName, SampleLocation startPos, SampleLocation endPos) {

    // chunks and positions
    auto start_chunk = startPos.getChunkLoc();
    auto start_sample_pos =  startPos.getSampleLoc();

    auto end_chunk = endPos.getChunkLoc();
    auto end_sample_pos = endPos.getSampleLoc();

    auto sample_count = ChunkMetric::MAX_SAMPLES*(end_chunk-start_chunk-2)
                        + (ChunkMetric::MAX_SAMPLES - start_sample_pos)
                        + (end_sample_pos+1);

    Dataset::MetricsPtr p = new std::vector<uint64_t>;
    p->reserve(sample_count);

    // first chunk
    auto c = chunkVector[start_chunk]->getMetric(metricName);
    p->insert(p->end(), c, c+(ChunkMetric::MAX_SAMPLES - start_sample_pos));

    // Append chunks
    for (int i=start_chunk+1; i<end_chunk; ++i) {
        c = chunkVector[i]->getMetric(metricName);
        p->insert(p->end(), c, c+ChunkMetric::MAX_SAMPLES);
    }

    // Append last chunk
    c = chunkVector[start_chunk]->getMetric(metricName);
    p->insert(p->end(), c, c+(end_sample_pos+1));

    return p;
}


void
Dataset::FileParsed(const char * filePath,
                    uint64_t start, uint64_t end,
                    size_t samples) {

    int metricsNameLen = 0;
    for (auto chunk : chunkVector) {

        auto currMetricLen = chunk->getMetricsCount();
        if (metricsNameLen != 0  && metricsNameLen!=currMetricLen) {
            BOOST_LOG_TRIVIAL(debug) << "Number of metrics differ from chunk to chunk:" << metricsNameLen << "!= " << currMetricLen;
        }

        if (metricsNameLen!=currMetricLen) {
            metricNames.clear();
            chunk->getMetricNames(metricNames);
            metricsNameLen = currMetricLen;
        }
    }

    auto fileData = new FileParsedData(filePath, start, end, samples);
    filesParsed.emplace_back(fileData);
}


bool
Dataset::setParser(const bool b) {
    auto prev = LazyParsing;
    LazyParsing = b;
    return prev;
}

std::vector<FileParsedData*>
Dataset::getParsedFileInfo() {
    return this->filesParsed;
}

