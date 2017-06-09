#pragma once

#include "cqp.h"

class CQApp {
public:
    CQApp() {};

    CQApp(int32_t authcode) {
        this->_ac = authcode;
    }

    int32_t sendPrivateMsg(int64_t qq, const char *msg) {
        return CQ_sendPrivateMsg(this->_ac, qq, msg);
    }

    int32_t sendGroupMsg(int64_t group_id, const char *msg) {
        return CQ_sendGroupMsg(this->_ac, group_id, msg);
    }

    int32_t sendDiscussMsg(int64_t discuss_id, const char *msg) {
        return CQ_sendDiscussMsg(this->_ac, discuss_id, msg);
    }

    int32_t sendLike(int64_t qq) {
        return CQ_sendLike(this->_ac, qq);
    }

    int32_t sendLikeV2(int64_t qq, int32_t times) {
        return CQ_sendLikeV2(this->_ac, qq, times);
    }

    int32_t setGroupKick(int64_t group_id, int64_t qq, cq_bool_t reject_add_request) {
        return CQ_setGroupKick(this->_ac, group_id, qq, reject_add_request);
    }

    int32_t setGroupBan(int64_t group_id, int64_t qq, int64_t duration) {
        return CQ_setGroupBan(this->_ac, group_id, qq, duration);
    }

    int32_t setGroupAnonymousBan(int64_t group_id, const char *anonymous, int64_t duration) {
        return CQ_setGroupAnonymousBan(this->_ac, group_id, anonymous, duration);
    }

    int32_t setGroupWholeBan(int64_t group_id, cq_bool_t enable) {
        return CQ_setGroupWholeBan(this->_ac, group_id, enable);
    }

    int32_t setGroupAdmin(int64_t group_id, int64_t qq, cq_bool_t set) {
        return CQ_setGroupAdmin(this->_ac, group_id, qq, set);
    }

    int32_t setGroupAnonymous(int64_t group_id, cq_bool_t enable) {
        return CQ_setGroupAnonymous(this->_ac, group_id, enable);
    }

    int32_t setGroupCard(int64_t group_id, int64_t qq, const char *new_card) {
        return CQ_setGroupCard(this->_ac, group_id, qq, new_card);
    }

    int32_t setGroupLeave(int64_t group_id, cq_bool_t is_dismiss) {
        return CQ_setGroupLeave(this->_ac, group_id, is_dismiss);
    }

    int32_t setGroupSpecialTitle(int64_t group_id, int64_t qq, const char *new_special_title, int64_t duration) {
        return CQ_setGroupSpecialTitle(this->_ac, group_id, qq, new_special_title, duration);
    }

    int32_t setDiscussLeave(int64_t discuss_id) {
        return CQ_setDiscussLeave(this->_ac, discuss_id);
    }

    int32_t setFriendAddRequest(const char *response_flag, int32_t response_operation, const char *remark) {
        return CQ_setFriendAddRequest(this->_ac, response_flag, response_operation, remark);
    }

    int32_t setGroupAddRequest(const char *response_flag, int32_t request_type, int32_t response_operation) {
        return CQ_setGroupAddRequest(this->_ac, response_flag, request_type, response_operation);
    }

    int32_t setGroupAddRequestV2(const char *response_flag, int32_t request_type, int32_t response_operation, const char *reason) {
        return CQ_setGroupAddRequestV2(this->_ac, response_flag, request_type, response_operation, reason);
    }

    int64_t getLoginQQ() {
        return CQ_getLoginQQ(this->_ac);
    }

    const char *getLoginNick() {
        return CQ_getLoginNick(this->_ac);
    }

    const char *getStrangerInfo(int64_t qq, cq_bool_t no_cache) {
        return CQ_getStrangerInfo(this->_ac, qq, no_cache);
    }

    const char *getGroupList() {
        return CQ_getGroupList(this->_ac);
    }

    const char *getGroupMemberList(int64_t group_id) {
        return CQ_getGroupMemberList(this->_ac, group_id);
    }

    const char *getGroupMemberInfoV2(int64_t group_id, int64_t qq, cq_bool_t no_cache) {
        return CQ_getGroupMemberInfoV2(this->_ac, group_id, qq, no_cache);
    }

    const char *getCookies() {
        return CQ_getCookies(this->_ac);
    }

    int32_t getCsrfToken() {
        return CQ_getCsrfToken(this->_ac);
    }

    const char *getAppDirectory() {
        return CQ_getAppDirectory(this->_ac);
    }

    const char *getRecord(const char *file, const char *out_format) {
        return CQ_getRecord(this->_ac, file, out_format);
    }

    int32_t addLog(int32_t log_level, const char *category, const char *log_msg) {
        return CQ_addLog(this->_ac, log_level, category, log_msg);
    }

    int32_t setFatal(const char *error_info) {
        return CQ_setFatal(this->_ac, error_info);
    }

    int32_t setRestart() {
        return CQ_setRestart(this->_ac);
    }

private:
    int32_t _ac;
};
