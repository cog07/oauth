package com.oauthservice.repository;

import java.util.Optional;

import com.oauthservice.model.AppUser;
import org.springframework.data.jpa.repository.JpaRepository;

public interface AppUserRepository
        extends JpaRepository<AppUser, Long> {

    Optional<AppUser> findByUsername(String username);

}