<?php
namespace app\company\controller;

use app\common\Mail;
use app\common\model\ManuscriptInfo;
use think\Controller;
use think\Exception;
use think\facade\Session;
use app\common\AES;
use app\common\model\Manuscript;

class Review extends controller
{
    public function index()
    {
        return $this->fetch();
    }

    public function test()
    {
    }


    /*Interface: 创建评审信息
    Function: createReview
    Url: company/review/createReview
    Type: post
    Input: {manuscriptId, result, suggestion}
    Output: {errNo, msg}
        errNo: 0, msg: '创建成功'
        errNo: 1, msg: '参数错误;
        errNo: 10, msg: '稿件不存在'
        errNo: 10, msg: '邮件发送失败'
    NOTE: result: 0-未录用, 1-录用, 2-修改后录用
    */
    public function createReview()
    {
        if ($this->request->isAjax()) {
            $data = input();
            if (isset($data['manuscriptId']) && isset($data['result']) && isset($data['suggestion'])) {
                $manuscriptId = AES::decrypt($data['manuscriptId']);
                $manuscript = Manuscript::get($manuscriptId);
                $manuscriptInfo = $manuscript->manuscriptInfo()->find();
                $manuscriptInfoId = $manuscriptInfo->manuscript_info_id;
                $meeting = $manuscript->meeting()->find();
                $title = $meeting->title;
                if (!isset($manuscript)) {
                    return json(['errNo' => 10, 'msg' => '稿件不存在']);
                }
                $review = new \app\common\model\Review();
                $review->manuscript_id = $manuscriptId;
                $review->result = $data['result'];
                $review->suggestion = $data['suggestion'];
                $review->save();
                $tempdata = array('manuscriptId' => $manuscriptId);
                try {
                    $this->sendReviewResult($tempdata);
                } catch (\Exception $e) {
                    return json(['errNo' => 10, 'msg' => '发送审核结果失败']);
                }

                try {
                    if ($data['result'] == 1)
                        $this->sendAcceptInform($manuscriptInfoId, $title);
                } catch (\Exception $e) {
                    return json(['errNo' => 10, 'msg' => '发送录用确认失败']);
                }

                return json(['errNo' => 0, 'msg' => '创建成功']);
            } else return json(['errNo' => 1, 'msg' => '参数错误']);
        } else return $this->error('页面错误');
    }

    /*Interface: 通过稿件ID获取评审信息
    Function: getReviewDetailByManuscriptId
    Url: company/review/getReviewDetailByManuscriptId
    Type: post
    Input: {manuscriptId}
    Output: {errNo, msg, data: {reviewId, manuscriptId, result, suggestion, createTime, updateTime}}
        errNo: 0, msg: '获取成功', data: {reviewId, manuscriptId, result, suggestion, createTime, updateTime}
        errNo: 1, msg: '参数错误', data: null
        errNo: 10, msg: '评审信息不存在', data: null
    */

    public function getReviewDetailByManuscriptId()
    {
        if ($this->request->isAjax()) {
            $data = input();
            if (isset($data['manuscriptId'])) {
                $manuscriptId = AES::decrypt($data['manuscriptId']);
                $manuscript = Manuscript::get($manuscriptId);
                if (!isset($manuscript)) {
                    return json(['errNo' => 10, 'msg' => '稿件不存在']);
                }
                $review = $manuscript->review()->find();
                if (!isset($review)) {
                    return json(['errNo' => 10, 'msg' => '评审信息不存在']);
                }
                $returnData = array(
                    'reviewId' => AES::encrypt($review->review_id),
                    'manuscriptId' => AES::encrypt($review->manuscript_id),
                    'result' => $review->result,
                    'suggestion' => $review->suggestion,
                    'createTime' => $review->create_time,
                    'updateTime' => $review->update_time,
                );
                return json(['errNo' => 0, 'msg' => '获取成功']);
            } else return json(['errNo' => 1, 'msg' => '参数错误']);
        } else return $this->error('页面错误');
    }

    /*Interface: 获取评审信息
    Function: getReviewDetail
    Url: company/review/getReviewDetail
    Type: post
    Input: {reviewId}
    Output: {errNo, msg, data: {reviewId, manuscriptId, result, suggestion, createTime, updateTime}}
        errNo: 0, msg: '获取成功', data: {reviewId, manuscriptId, result, suggestion, createTime, updateTime}
        errNo: 1, msg: '参数错误', data: null
        errNo: 10, msg: '稿件不存在', data: null
        errNo: 10, msg: '评审信息不存在', data: null
    */
    public function getReviewDetail()
    {
        if ($this->request->isAjax()) {
            $data = input();
            if (isset($data['reviewId'])) {
                $reviewId = AES::decrypt($data['reviewId']);
                $man = \app\common\model\Review::get($reviewId);
                if (!isset($review)) {
                    return json(['errNo' => 10, 'msg' => '评审信息不存在']);
                }
                $returnData = array(
                    'reviewId' => AES::encrypt($review->review_id),
                    'manuscriptId' => AES::encrypt($review->manuscript_id),
                    'result' => $review->result,
                    'suggestion' => $review->suggestion,
                    'createTime' => $review->create_time,
                    'updateTime' => $review->update_time,
                );
                return json(['errNo' => 0, 'msg' => '创建成功']);
            } else return json(['errNo' => 1, 'msg' => '参数错误']);
        } else return $this->error('页面错误');
    }

    /*Interface: 通过稿件ID通过邮件向用户评审信息(已改为对内接口）
    Function: sendReviewResult
    Url: company/review/sendReviewResult
    Type: post
    Input: {manuscriptId}
    Output: {errNo, msg, data }
        errNo: 0, msg: '发送成功', data: null
        errNo: 1, msg: '参数错误', data: null
        errNo: 10, msg: '稿件不存在', data: null
        errNo: 10, msg: '评审信息不存在', data: null
    */
    public function sendReviewResult($data)
    {
        if (isset($data['manuscriptId'])) {
            //$manuscriptId = AES::decrypt($data['manuscriptId']);
            $manuscriptId = $data['manuscriptId'];
            $manuscript = Manuscript::get($manuscriptId);
            $meeting = $manuscript->meeting()->find();
            $meetingName = $meeting->title;
            $manuscriptInfo = $manuscript->manuscriptInfo()->find();
            $manuscriptName = $manuscriptInfo->title;
            if (!isset($manuscript)) {
                return json(['errNo' => 10, 'msg' => '稿件不存在']);
            }
            $review = $manuscript->review()->find();
            if (!isset($review)) {
                return json(['errNo' => 10, 'msg' => '评审信息不存在']);
            }
            $user = $manuscript->user()->find();
            $userId = $user->user_id;

            $reviewData = array(
                'reviewId' => AES::encrypt($review->review_id),
                'manuscriptId' => AES::encrypt($review->manuscript_id),
                'result' => $review->result,
                'suggestion' => $review->suggestion,
                'createTime' => $review->create_time,
                'updateTime' => $review->update_time,
            );
            Mail::sendReviewResultMail($userId, $reviewData, $manuscriptName, $meetingName);

            return json(['errNo' => 0, 'msg' => '创建成功']);
        } else return json(['errNo' => 1, 'msg' => '参数错误']);

    }

    public function sendAcceptInform($manuscriptInfoId, $meetingTitle)
    {
        $manuscriptInfo = ManuscriptInfo::get($manuscriptInfoId);
        $author = json_decode($manuscriptInfo->author, true);
        $essayTitle = $manuscriptInfo->title;
        foreach ($author as $item) {
            Mail::sendAcceptInformMail($item, $essayTitle, $meetingTitle);
        }
    }





}