<?php
namespace app\common\controller;

class AES {
    private $_iv = '';
    private $_secret = '';

    public function __construct(/*$iv, $secret*/) {
        $iv = 'meeting_password';
        $secret = 'meeting_password';
        $this->_iv = substr($iv.'0000000000000000',  0, 16);//可以忽略这一步，只要你保证iv长度是16
        $this->_secret = hash('md5', $secret, true);
    }

    public function decrypt($data) {
        return openssl_decrypt(base64_decode($data), 'aes-128-cbc', $this->_secret, false, $this->_iv);
    }

    public function encrypt($data) {
        return base64_encode(openssl_encrypt($data, 'aes-128-cbc', $this->_secret, false, $this->_iv));
    }
}