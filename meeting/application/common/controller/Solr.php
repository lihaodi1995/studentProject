<?php
namespace app\common\controller;

use app\common\controller\SolrBase;

header("Content-type:text/html;charset=utf-8");

class Solr {
    public function search($coreName, $searchString, $limit, $page) {
        if ($limit <= 0 || $page <= 0) return null;
        $solrBase = new SolrBase('http://localhost:8983/solr/', $coreName, 1);

        $searchString = trim($searchString);
        $searchArray = explode(' ', $searchString);
        $searchString = '';
        foreach ($searchArray as $key => $keyWord) {
            $keyWord = urlencode(trim($keyWord));
            if (!strlen($keyWord)) continue;
            if (!strlen($searchString)) {
                $searchString = $keyWord . '%20*' . $keyWord . '*';
            }
            else $searchString.='%20'. $keyWord . '%20*' . $keyWord . '*'; 
        }
        //echo $searchString . "\n";

        $start = ($page - 1) * $limit;
        $rows = $limit;
        $ret = $solrBase->solrQuery('q=' . $searchString, $start, $rows);
        return $ret;

        /*
        $searchk =  isset($_POST['searchk']) ? addslashes(trim($_POST['searchk'])) : NULL;

        //solr search BEGIN////////////////////////////////////////////////////
        //$query = q=urlencode(pinyin:*$searchk*).&sort=urlencode($sort)
        //判断值含有汉字 -- Y:keyword  N:pinyin
        $flag = true; //搜索方式标记  true：keyword false:pinyin
        if ($searchk != null) {
            if (preg_match("/([\x81-\xfe][\x40-\xfe])/", $searchk, $match)) {
                $q = 'keyword:' . $searchk . '*';
            } else {
                $q = 'pinyin:' . strtolower($searchk) . '*';
                $flag = false;
            }
        } else {
            echo json_encode(array());
            exit();
        }
        $sort = 'weight desc';
        $query = '&q=' . urlencode($q) . '&sort=' . urlencode($sort);
        //显示条数

        //返回查询的数据
        $searchdataarr = $solrBase->solrQuery($query, $start, $rows);
        //solr search END////////////////////////////////////////////////////////
        */
    }
}