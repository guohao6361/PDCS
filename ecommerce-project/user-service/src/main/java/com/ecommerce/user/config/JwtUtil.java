package com.ecommerce.user.config;

import io.jsonwebtoken.Claims;
import io.jsonwebtoken.JwtException;
import io.jsonwebtoken.Jwts;
import io.jsonwebtoken.security.Keys;
import jakarta.annotation.PostConstruct;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;

import javax.crypto.SecretKey;
import java.nio.charset.StandardCharsets;
import java.util.Date;

@Component
public class JwtUtil {

    private static final Logger log = LoggerFactory.getLogger(JwtUtil.class);
    private static final String WEAK_DEFAULT_SECRET = "myDefaultJwtSecretKeyForDevelopmentOnly123456";
    private static final int MIN_SECRET_LENGTH = 32;

    @Value("${app.jwt.secret}")
    private String jwtSecret;

    @Value("${app.jwt.expiration:86400000}")
    private long jwtExpiration;

    @PostConstruct
    public void validateSecret() {
        if (WEAK_DEFAULT_SECRET.equals(jwtSecret)) {
            log.warn("⚠️ JWT 使用默认弱密钥，仅限开发环境使用！生产环境请设置 JWT_SECRET 环境变量");
        } else if (jwtSecret.length() < MIN_SECRET_LENGTH) {
            throw new IllegalStateException(
                    "JWT 密钥长度不足 " + MIN_SECRET_LENGTH + " 位，当前长度: " + jwtSecret.length());
        }
    }

    public String generateToken(Integer userId, String username) {
        return Jwts.builder()
                .subject(username)
                .claim("userId", userId)
                .issuedAt(new Date())
                .expiration(new Date(System.currentTimeMillis() + jwtExpiration))
                .signWith(getSigningKey())
                .compact();
    }

    public Claims parseToken(String token) {
        return Jwts.parser()
                .verifyWith(getSigningKey())
                .build()
                .parseSignedClaims(token)
                .getPayload();
    }

    public boolean validateToken(String token) {
        try {
            parseToken(token);
            return true;
        } catch (JwtException e) {
            return false;
        }
    }

    private SecretKey getSigningKey() {
        return Keys.hmacShaKeyFor(jwtSecret.getBytes(StandardCharsets.UTF_8));
    }
}
