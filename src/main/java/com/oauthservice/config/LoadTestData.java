package com.oauthservice.config;

import com.oauthservice.model.AppUser;
import com.oauthservice.repository.AppUserRepository;
import org.springframework.boot.CommandLineRunner;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.crypto.password.PasswordEncoder;

@Configuration
public class LoadTestData {
    @Bean
    CommandLineRunner init(AppUserRepository repository, PasswordEncoder passwordEncoder){
        return args -> {
            if(repository.count() == 0 ){
                repository.save(new AppUser(
                        "appusr",passwordEncoder.encode("pass"),"admin"
                ));
            }
        };
    }

}
