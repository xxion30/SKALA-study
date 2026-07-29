package com.example.demo.service;

import org.springframework.stereotype.Service;

import com.example.demo.repository.UserRepository;

@Service("userService")
public class UserService {
    //의존 객체
    private UserRepository userRepository;

    //생성자를 유의해서 의존 주의
    public UserService(UserRepository userRepository) {
        this.userRepository = userRepository;
    }

    //서비스 메서드 <- 비즈니스 로직을 처리하는 메서드
    public void printUser() {
        System.out.println("사용자: " + userRepository.findUser());
    }
}
