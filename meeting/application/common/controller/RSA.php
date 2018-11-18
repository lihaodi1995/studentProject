<?php
namespace app\common\controller;

class RSA {
    protected $publicKey = '';
    protected $privateKey = '';

    public function __construct() {
        $publicKeyFile = fopen('../others/RSA/PublicKey.txt', 'r');
        $privateKeyFile = fopen('../others/RSA/PrivateKey.txt', 'r');
        if (filesize('../others/RSA/PublicKey.txt') > 0 && filesize('../others/RSA/PrivateKey.txt') > 0) {
            $this->publicKey = fread($publicKeyFile, filesize('../others/RSA/PublicKey.txt'));
            $this->privateKey = fread($privateKeyFile, filesize('../others/RSA/PrivateKey.txt'));
        } else {
            $config = array(
                "digest_alg" => "sha512",
                "private_key_bits" => 2048,
                "private_key_type" => OPENSSL_KEYTYPE_RSA,
            );
            $resource = openssl_pkey_new($config);
            openssl_pkey_export($resource, $this->privateKey);
            $detail = openssl_pkey_get_details($resource);
            $this->publicKey = $detail['key'];
            $publicKeyFile = fopen('../others/RSA/PublicKey.txt', "w");
            $privateKeyFile = fopen('../others/RSA/PrivateKey.txt', "w");
            fwrite($publicKeyFile, $this->publicKey);
            fwrite($privateKeyFile, $this->privateKey);
        }
    }

    public function publicEncrypt($data){
        $str = '';
        openssl_public_encrypt($data, $str, $this->publicKey);
        $str = base64_encode($str);
        return $str;
    }

    public function privateDecrypt($data){
        $str = '';
        $data = base64_decode($data);
        openssl_private_decrypt($data, $str, $this->privateKey);
        return $str;
    }

    function strToHex($str){ 
        $hex = '';
        $length = strlen($str);
        for($i = 0; $i < $length; $i++)
            $hex .= dechex(ord($str[$i]));
        $hex = strtoupper($hex);
        return $hex;
    }   
     
    function hexToStr($hex){   
        $str = '';
        $length = strlen($hex);
        for($i = 0; $i < $length - 1; $i += 2)
            $str .= chr(hexdec($hex[$i].$hex[$i + 1]));
        return $str;
    }
}