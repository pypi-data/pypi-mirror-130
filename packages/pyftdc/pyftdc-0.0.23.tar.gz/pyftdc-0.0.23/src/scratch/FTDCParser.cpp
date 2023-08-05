//
// Created by jorge on 11/2/20.
//
#include <FTDCParser.h>
#include <ParserTasksList.h>
#include <sys/stat.h>
#include <string>

#include <boost/log/core.hpp>
#include <boost/log/trivial.hpp>
#include <boost/log/expressions.hpp>
// From libbson
#include <bson/bson.h>
#include <boost/thread.hpp>
#include <boost/algorithm/string/split.hpp>
#include <boost/algorithm/string/classification.hpp>

#include <sys/time.h>
#include <sys/resource.h>

namespace logging = boost::log;

#define FALSE 0

static double double_time_of_day() {
    struct timeval timeval{};
    bson_gettimeofday(&timeval);
    return (timeval.tv_sec + timeval.tv_usec * 0.000001);
}

int
FTDCParser::parseInfoChunk(const bson_t *bson) {

    size_t length=0;
    auto json = bson_as_json(bson, &length);
    BOOST_LOG_TRIVIAL(debug) << json;

    this->metadata.push_back(std::string(json));

    bson_free(json);

    return 0;
}

 int
 ParserTaskConsumerThread(ParserTasksList *parserTasks, Dataset *dataSet) {

    bool logChunkMetrics = FALSE;
    while (!parserTasks->empty()) {

        ParserTask  *task = parserTasks->pop();

        auto chunk = new Chunk(task->getData(), task->getDataSize(), task->getId(), logChunkMetrics);

        // only once
        logChunkMetrics = FALSE;

        // Decompress and check sizes
        if (chunk->Decompress() > 0) {
            auto data = chunk->getUncompressedData();

            // We construct the metrics. This are name and first value only since deltasInChunk have not been read.
            chunk->ConstructMetrics(data);

            // Get actual values
            chunk->ReadVariableSizedInts();
            chunk->setTimestampLimits();
            dataSet->addChunk(chunk);
        } else {
            delete chunk;
            BOOST_LOG_TRIVIAL(error) << "Could not decompress chunk! "  << "Task:" << task->getId() << " " << task->getDataSize();;
        }

        // This was allocated in the main thread.
        delete [] task->getData();
    }
    
    return 0;
}


bson_reader_t *
FTDCParser::open(std::string file_path) {

    bson_error_t error;

    // File exists?
    struct stat data{};
    if (stat(file_path.c_str(), &data) != 0) {
        BOOST_LOG_TRIVIAL(error) << "Failed to find file'" << file_path << "' " << error.code;
        return nullptr;
    }

    // Initialize a new reader for this file descriptor.
    bson_reader_t *reader;
    if (!(reader = bson_reader_new_from_file(file_path.c_str(), &error))) {
        BOOST_LOG_TRIVIAL(error) << "Failed to open file '" << file_path << "' " << error.code;
        return nullptr;
    }
    return reader;
}

int
FTDCParser::parseFiles(std::string file_paths,  bool metadata, bool metric_names, const bool lazy_parsing) {
    std::vector<std::string> vector_files;

    boost::split(vector_files, file_paths, boost::is_any_of(","));

    auto ret = parseFiles(&vector_files,metadata,metric_names);
    return ret;
}

int
FTDCParser::parseFiles(std::vector<std::string> const *file_paths,   const bool only_metadata, const bool only_metric_names, const bool lazy_parsing) {
    bson_reader_t *reader;
    const bson_t *pBsonChunk;

    double date_time_before, date_time_after, date_time_delta;

    namespace logging = boost::log;
    logging::core::get()->set_filter(logging::trivial::severity >  logging::trivial::debug);

    for (auto file_name : *file_paths) {
        BOOST_LOG_TRIVIAL(info) << "File: " << file_name;

        reader = this->open(file_name);
        if (!reader) return -1;

        date_time_before = double_time_of_day();

        bool at_EOF = false;
        unsigned int chunkCount = 0;
        bool parsing_values = false;

        uint64_t first_id = Dataset::INVALID_TIMESTAMP;
        uint64_t current_id = Dataset::INVALID_TIMESTAMP;

        while ((pBsonChunk = bson_reader_read(reader, &at_EOF))) {

            BOOST_LOG_TRIVIAL(debug) << "Chunk # " << chunkCount << " length: " << pBsonChunk->len;
            if (!parsing_values) {
                parseInfoChunk(pBsonChunk);
                parsing_values = true;
                if (only_metadata) break;
            }
            else {

                bson_iter_t iter;

                if (bson_iter_init(&iter, pBsonChunk)) {
                    while (bson_iter_next(&iter)) {

                        if (BSON_ITER_HOLDS_BINARY(&iter)) {
                            bson_subtype_t subtype;
                            uint32_t bin_size;
                            const uint8_t *data;
                            bson_iter_binary(&iter, &subtype, &bin_size, reinterpret_cast<const uint8_t **>(&data));

                            // the memory pointed to by data is managed internally. Better make a copy
                            uint8_t *bin_data = new uint8_t [bin_size];
                            memcpy(bin_data, data, bin_size);
                            parserTasks.push(bin_data, bin_size, current_id);

                        } else if (BSON_ITER_HOLDS_DATE_TIME(&iter)) {
                            current_id = bson_iter_date_time(&iter);
                            if (first_id == Dataset::INVALID_TIMESTAMP) first_id = current_id;
                        } else if (BSON_ITER_HOLDS_INT32(&iter)) {
                            ; // type = bson_iter_int32(&iter);
                        }
                    }
                }
                
                if (only_metric_names)
                    break;
            }
            ++chunkCount;
        }

        if (!lazy_parsing) {
            // Thread pool
            size_t numThreads = boost::thread::hardware_concurrency();
            boost::thread_group threads;
            for (size_t i = 0; i < numThreads; ++i)
                threads.add_thread(new boost::thread(ParserTaskConsumerThread, &parserTasks, &dataSet));
            // Wait for threads to finish
            threads.join_all();

            dataSet.sortChunks();
            date_time_after = double_time_of_day();
        }

        dataSet.setParser(lazy_parsing);

        if (!at_EOF)
            BOOST_LOG_TRIVIAL(error) << "Not all chunks were parsed.";

        // This is the end of a file being parsed.
        dataSet.FileParsed(file_name.c_str(), first_id, current_id, chunkCount);

        date_time_delta = BSON_MAX ((double) (date_time_after - date_time_before), 0.000001);
        BOOST_LOG_TRIVIAL(info) << "File parsed in " << date_time_delta
                 << " secs. There are " << dataSet.getChunkCount() << " chunks, "
                 << dataSet.getMetricNamesCount() << " metrics with "
                 << dataSet.getMetricLength() << " samples";

        struct rusage usage;
        getrusage(RUSAGE_SELF, &usage);

        BOOST_LOG_TRIVIAL(info) << "maximum resident set size: " << usage.ru_maxrss
                                << "  integral shared memory size: " << usage.ru_ixrss
                                << "  integral unshared data size: " << usage.ru_idrss
                                << "  integral unshared stack size" << usage.ru_isrss;

        if (only_metric_names) {
            std::vector<std::string> names;
            dataSet.getMetricNames(names);
            int i=0;
            for (auto name : names ) {
                BOOST_LOG_TRIVIAL(info) << "(" << ++i << "/" << names.size() << "):  " <<  name;
            }
        }

        // Cleanup after our reader, which closes the file descriptor.
        bson_reader_destroy(reader);
    } //

    return 0;
}

std::vector<std::string>
FTDCParser::getMetricsNamesPrefixed(std::string prefix) {
    std::vector<std::string> names;

    std::vector<std::string> metricNames;
    dataSet.getMetricNames(metricNames);

    for (auto & m : metricNames) {
        if (prefix == m.substr(0, prefix.size()))
            names.push_back(m);
    }
    return names;
}

std::vector<std::string>
FTDCParser::getMetricsNames() {
    std::vector<std::string> metricNames;
    dataSet.getMetricNames(metricNames);
    return metricNames;
}

Dataset::MetricsPtr
FTDCParser::getMetric(std::string name, uint64_t start, uint64_t end) {
     return dataSet.getMetric(name, start, end);
}

std::vector<FileParsedData*>
FTDCParser::getParsedFileInfo() {
    return dataSet.getParsedFileInfo();

}
