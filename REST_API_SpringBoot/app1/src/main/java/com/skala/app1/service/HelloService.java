package com.skala.app1.service;

import org.springframework.stereotype.Service;

@Service
public class HelloService {
    public String hello() {
        return "Say hello from HelloService";
    }
}
