//
// Created by jorge on 12/16/20.
//

#ifndef FTDCPARSER_DATASET_H
#define FTDCPARSER_DATASET_H

#include <string>
#include <vector>
#include <map>
#include <boost/thread/mutex.hpp>
#include "Chunk.h"
#include "MergerTasksList.h"
#include "SampleLocation.h"
#include "FileParsedData.h"


class Dataset   {

public:
    typedef std::vector<uint64_t> Metrics;
    typedef std::vector<uint64_t>* MetricsPtr;

    std::vector<FileParsedData*> getParsedFileInfo();
    Dataset() : samplesInDataset(0),  metricNames(0), LazyParsing(false) {};
    void addChunk(Chunk *pChunk);
    size_t getChunkCount() { return chunkVector.size(); }
    Chunk *getChunk(size_t n) { return (n < chunkVector.size()) ? chunkVector[n] : nullptr; }
    std::vector<Chunk *> getChunkVector() { return chunkVector; }
    size_t getMetricNames(std::vector< std::string> & metricNames);
    [[nodiscard]] size_t getMetricLength() const { return samplesInDataset; }

    MetricsPtr getMetric(std::string   metricName, uint64_t start, uint64_t end);

    std::map<std::string, MetricsPtr> getHashMetrics() { return hashMapMetrics; }
    size_t getMetricNamesCount() { return metricNames.size(); }
    void sortChunks();
    void FileParsed(const char * path, uint64_t start, uint64_t end, size_t samplesInFile);
    void addMergedMetric(std::string   metricName, MetricsPtr data);
    bool setParser(const bool i);

    MetricsPtr assembleMetricFromChunks(std::string metricName, SampleLocation startPos, SampleLocation endPos);

private:
    void releaseChunks();
    SampleLocation getLocationInChunks(uint64_t sample, bool fromStart); // returns position as a tuple of (chunk index, pos)

public:

    static const uint64_t FIRST_TIMESTAMP = UINT64_MAX;
    static const uint64_t LAST_TIMESTAMP = UINT64_MAX;
    static const uint64_t INVALID_TIMESTAMP = UINT64_MAX;
    static const int INVALID_CHUNK_NUMBER = INT_MAX;
    static const int INVALID_TIMESTAMP_POS = INT_MAX;


private:
    bool LazyParsing;
    std::vector<Chunk*> chunkVector;
    size_t samplesInDataset;
    boost::mutex mu;
    std::vector<std::string> metricNames;
    std::map<std::string,  MetricsPtr>  hashMapMetrics;

    std::vector<FileParsedData*> filesParsed;
};


#endif //FTDCPARSER_DATASET_H
