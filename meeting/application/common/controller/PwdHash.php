<?php
namespace app\common\controller;

class PwdHash {
    public function getSalt($str) {
        $salt = MD5($str . date('Y-m-d H:i:s', time()));
        $length = strlen($salt);
        $salt = substr($salt, rand(0, $length / 3 - 1), $length * 2/ 3);
        $salt = MD5($salt);
        $salt = substr($salt, rand(0, $length / 3 - 1), $length * 2/ 3);
        return $salt;
    }

    public function getHashCode($str, $salt){
        $code = "";
        $strLength = strlen($str);
        $saltLength = strlen($salt);
        for ($i = 0; $i < $strLength && $i < $saltLength; $i++){ $code .= $str[$i]; $code .= $salt[$i]; }
        while ($i < $strLength){ $code .= $str[$i]; $i++; }
        while ($i < $saltLength){ $code .= $salt[$i]; $i++; }
        return sha1($code);
    }
}