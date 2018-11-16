package com.example.demo.utils;

import java.util.Map;
import java.util.Objects;

/**
 * @Author : 叶明林
 * @Description: 主要用于快速生成键值对
 * @Date created at 2018/5/18 14:15
 **/
public class Node<K,V> implements Map.Entry<K,V> {
    private final K key;
    private V value;

    public Node(K key, V value) {
        this.key = key;
        this.value = value;
    }

    public final K getKey()        { return key; }
    public final V getValue()      { return value; }
    public final String toString() { return key + "=" + value; }

    public final int hashCode() {
        return Objects.hashCode(key) ^ Objects.hashCode(value);
    }

    public final V setValue(V newValue) {
        V oldValue = value;
        value = newValue;
        return oldValue;
    }

    public final boolean equals(Object o) {
        if (o == this)
            return true;
        if (o instanceof Map.Entry) {
            Map.Entry<?,?> e = (Map.Entry<?,?>)o;
            return Objects.equals(key, e.getKey()) &&
                    Objects.equals(value, e.getValue());
        }
        return false;
    }
}