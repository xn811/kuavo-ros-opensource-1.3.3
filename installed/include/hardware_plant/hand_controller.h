#ifndef BRAINCO_HAND_CONTROLLER_H_
#define BRAINCO_HAND_CONTROLLER_H_
#include <stdint.h>
#include <memory>
#include <string>
#include <thread>
#include <atomic>
#include <mutex>
#include <queue>
#include <unordered_map>
#include <condition_variable>

#include "hand_sdk.h"
#include "gesture_types.h"

namespace eef_controller {

enum class HandSide: int {
    LEFT = 0,
    RIGHT = 1,
    BOTH = 2
};

struct ActionSequenceData{
    uint16_t duration_ms; // ms
    int8_t positions[6]; 
    int8_t speeds[6];
    int8_t forces[6];

    ActionSequenceData(): duration_ms(500) {
        for (int i = 0; i < 6; i++) {
            positions[i] = 0;
            speeds[i] = 0;
            forces[i] = 0;
        }
    }
};

struct GestureInfo {
    std::string gesture_name;               // 手势名称
    std::string description;                // 描述
    std::vector<std::string> alias;         // 别名列表
    std::vector<ActionSequenceData> action_sequences; // 手势序列的动作值
};
using GestureInfoPtr = std::shared_ptr<GestureInfo>;

struct GestureExecuteInfo {
    HandSide hand_side;
    std::string gesture_name;
};
using GestureExecuteInfoVec = std::vector<GestureExecuteInfo>;

class BrainCoController;
using BrainCoControllerPtr = std::unique_ptr<BrainCoController>;
class BrainCoController {
public:
    static BrainCoControllerPtr Create(const std::string &gesture_filepath) {
        return std::unique_ptr<BrainCoController>(new BrainCoController(gesture_filepath));
    }

    ~BrainCoController();

    bool init();
    bool close();
    void send_position(HandSide hand_side, int8_t *pos);
    void send_speed(HandSide hand_side, int8_t *speed);
    void send_current(HandSide hand_side, int8_t *current);

    /** 
     * @brief execute a gesture 
     * @param hand_side, the hand side to execute the gesture
     * @param gesture_name, the name of the gesture
     * @param [out] err_msg, the error message
     * @return true if success, false otherwise
     */
    bool execute_gesture(HandSide hand_side, const std::string &gesture_name, std::string &err_msg);
    
    /**
     * @brief  execute a list of gestures
     * 
     * @param gesture_tasks  the list of gestures to execute
     * @param err_msg        the error message
     * @return true if success, false otherwise 
     */
    bool execute_gestures(const GestureExecuteInfoVec& gesture_tasks, std::string &err_msg);

    /**
     * @brief get the list of gestures.
     * 
     * @return std::vector<GestureInfoMsg> 
     */
    std::vector<GestureInfoMsg> list_gestures();

    /**
     * @brief check if a gesture is currently executing.
     * 
     * @return true if a gesture is currently executing, false otherwise
     */
    bool is_gesture_executing();

private:
    BrainCoController(const std::string &gesture_filepath);
    void gesture_thread_func();
    bool sleep_for_100ms(int ms_count);

private:
    HandSDK *hand_sdk_ptr_ = nullptr;                               /* hand_sdk wrapper */
    std::string gesture_file_path_;                                 /* gesture config file */
    std::unordered_map<std::string, GestureInfoPtr> gesture_map_;   /* gesture info map */

    /* Task Queue Define! */
    struct GestureExecuteTask {
        HandSide        hand_side;  /* which hand */
        GestureInfoPtr  gesture;    /* gesture */
    };
    using BatchGestureTask = std::vector<GestureExecuteTask>;
    const int kTaskQueueSize_ = 1;            
    std::queue<BatchGestureTask> task_queue_;
    std::mutex task_queue_mtx_;
    std::condition_variable gesture_execute_cv_;
    std::atomic_bool abort_running_task_flag_ = false;  /* abort task execute! */
    std::atomic_bool gesture_executing_ = false;

    /* thread control */
    std::atomic_bool gesture_thread_exit_ = false;
    std::unique_ptr<std::thread> gesture_thread_ = nullptr;
};


} // namespace eef_controller

#endif