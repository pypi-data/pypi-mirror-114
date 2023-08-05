#pragma once

#include <depthai-shared/common/optional.hpp>
#include <nlohmann/json.hpp>

#include "depthai-shared/common/EepromData.hpp"

namespace dai {

/**
 * Specify properties which apply for whole pipeline
 */
struct GlobalProperties {
    /**
     * Set frequency of Leon OS - Increasing can improve performance, at the cost of higher power
     * draw
     */
    double leonCssFrequencyHz = 700 * 1000 * 1000;
    /**
     * Set frequency of Leon RT - Increasing can improve performance, at the cost of higher power
     * draw
     */
    double leonMssFrequencyHz = 700 * 1000 * 1000;
    tl::optional<std::string> pipelineName;
    tl::optional<std::string> pipelineVersion;
    /**
     * Calibration data sent through pipeline
     */

    tl::optional<dai::EepromData> calibData;

    /**
     * Camera tuning blob size in bytes
     */
    tl::optional<std::uint32_t> cameraTuningBlobSize;
    /**
     * Uri which points to camera tuning blob
     */
    std::string cameraTuningBlobUri;
};

NLOHMANN_DEFINE_TYPE_NON_INTRUSIVE(
    GlobalProperties, leonCssFrequencyHz, leonMssFrequencyHz, pipelineName, pipelineVersion, cameraTuningBlobSize, cameraTuningBlobUri, calibData);

}  // namespace dai
