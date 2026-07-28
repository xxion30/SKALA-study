package com.skala.app1.controller;


import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

//HelloService를 이용하도록 수정
import com.skala.app1.service.HelloService;



@RestController
@RequestMapping("/api")
public class HelloController {
    // 의존 객체를 필드로 정의
    private final HelloService helloService;

    // 생성자를 이용한 의존 주임
    public HelloController(HelloService helloService) {
        this.helloService = helloService;
    }


    @GetMapping("")
    public String home() {
        return "home";        
    }


    @GetMapping("/hello")
    public String hello() {
        // 의존 객체의 기능을 사용
        return helloService.hello();
    }
    @PostMapping("/post")
    public String post() {
        return "request by POST";
    }

    @DeleteMapping("/delete")
    public String delete() {
        return "request by DELETE";
    }

}
