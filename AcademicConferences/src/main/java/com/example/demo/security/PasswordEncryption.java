package com.example.demo.security;

import javax.crypto.SecretKeyFactory;
import javax.crypto.spec.PBEKeySpec;
import java.math.BigInteger;
import java.security.NoSuchAlgorithmException;
import java.security.SecureRandom;
import java.security.spec.KeySpec;

/**
 * @Author : 叶明林
 * @Description: 密码加密
 * @Date created at 2018/5/18 14:48
 **/
public class PasswordEncryption {
    private static final String ALGORITHM_ENCRY_PWD = "PBKDF2WithHmacSHA1";

    /**
     * 盐的长度
     */
    private static final int SALT_BYTE_SIZE = 32 / 2;

    /**
     * 生成密文的长度
     */
    private static final int HASH_BIT_SIZE = 128 * 4;

    /**
     * 迭代次数
     */
    private static final int PBKDF2_ITERATIONS = 2;

    public static String encryptPassword(String oldPassword,String salt) {
        try
        {
            KeySpec spec = new PBEKeySpec(oldPassword.toCharArray(), fromHex(salt), PBKDF2_ITERATIONS, HASH_BIT_SIZE);
            SecretKeyFactory f = SecretKeyFactory.getInstance(ALGORITHM_ENCRY_PWD);
            return toHex(f.generateSecret(spec).getEncoded());
        }
        catch (Exception e)
        {
            e.printStackTrace();
        }
        return null;

        //return  new SimpleHash(ALGORITHM_ENCRY_PWD, oldPassword).toHex();
    }

    /**
     * 通过提供加密的强随机数生成器 生成盐
     */
    public static String generateSalt()
    {
        try
        {
            SecureRandom random = SecureRandom.getInstance("SHA1PRNG");
            byte[] salt = new byte[SALT_BYTE_SIZE];
            random.nextBytes(salt);
            return toHex(salt);
        }
        catch (NoSuchAlgorithmException e)
        {
            e.printStackTrace();
        }
        return null;
    }

    /**
     * 十六进制字符串转二进制字符串
     */
    private static byte[] fromHex(String hex) {
        byte[] binary = new byte[hex.length() / 2];
        for (int i = 0; i < binary.length; i++) {
            binary[i] = (byte) Integer.parseInt(hex.substring(2 * i, 2 * i + 2), 16);
        }
        return binary;
    }

    /**
     * 二进制字符串转十六进制字符串
     */
    private static String toHex(byte[] array) {
        BigInteger bi = new BigInteger(1, array);
        String hex = bi.toString(16);
        int paddingLength = (array.length * 2) - hex.length();
        if (paddingLength > 0)
            return String.format("%0" + paddingLength + "d", 0) + hex;
        else
            return hex;
    }
}
