package com.ecommerce.user.config;

import com.ecommerce.common.ApiResponse;
import com.fasterxml.jackson.databind.ObjectMapper;
import io.jsonwebtoken.Claims;
import io.jsonwebtoken.JwtException;
import io.jsonwebtoken.Jwts;
import io.jsonwebtoken.security.Keys;
import jakarta.annotation.PostConstruct;
import jakarta.servlet.FilterChain;
import jakarta.servlet.ServletException;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;
import org.springframework.web.filter.OncePerRequestFilter;

import javax.crypto.SecretKey;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.util.List;

@Component
public class JwtAuthFilter extends OncePerRequestFilter {

    private static final Logger log = LoggerFactory.getLogger(JwtAuthFilter.class);
    private static final String WEAK_DEFAULT_SECRET = "myDefaultJwtSecretKeyForDevelopmentOnly123456";
    private static final int MIN_SECRET_LENGTH = 32;

    @Value("${app.jwt.secret}")
    private String jwtSecret;

    private final ObjectMapper objectMapper = new ObjectMapper();

    @PostConstruct
    public void validateSecret() {
        if (WEAK_DEFAULT_SECRET.equals(jwtSecret)) {
            log.warn("JWT 使用默认弱密钥，仅限开发环境使用！生产环境请设置 JWT_SECRET 环境变量");
        } else if (jwtSecret.length() < MIN_SECRET_LENGTH) {
            throw new IllegalStateException(
                    "JWT 密钥长度不足 " + MIN_SECRET_LENGTH + " 位，当前长度: " + jwtSecret.length());
        }
    }

    private static final List<String> PUBLIC_PATHS = List.of("/users/register", "/users/login");

    // 内部服务调用端点（跳过 JWT，仅限微服务网络内部访问）
    private boolean isInternalPath(String path) {
        return path.matches("/users/\\d+/deduct-balance")
                || path.matches("/users/\\d+/add-balance")
                || path.matches("/users/\\d+/verify-pay-password");
    }

    @Override
    protected void doFilterInternal(HttpServletRequest request,
                                    HttpServletResponse response,
                                    FilterChain filterChain) throws ServletException, IOException {
        if ("OPTIONS".equalsIgnoreCase(request.getMethod())) {
            filterChain.doFilter(request, response);
            return;
        }

        String path = request.getRequestURI();

        // 公开端点（注册/登录）无需 Token
        if (PUBLIC_PATHS.contains(path)) {
            filterChain.doFilter(request, response);
            return;
        }

        // 文件访问端点（头像等）无需 Token，供浏览器直接加载图片
        if (path.startsWith("/users/files/")) {
            filterChain.doFilter(request, response);
            return;
        }

        // 内部服务调用端点（跳过 JWT）
        if (isInternalPath(path)) {
            filterChain.doFilter(request, response);
            return;
        }

        // 其他端点强制要求 JWT Token
        String authHeader = request.getHeader("Authorization");
        if (authHeader == null || !authHeader.startsWith("Bearer ")) {
            writeUnauthorized(response, "请先登录");
            return;
        }

        String token = authHeader.substring(7);
        try {
            SecretKey key = Keys.hmacShaKeyFor(jwtSecret.getBytes(StandardCharsets.UTF_8));
            Claims claims = Jwts.parser()
                    .verifyWith(key)
                    .build()
                    .parseSignedClaims(token)
                    .getPayload();
            request.setAttribute("userId", claims.get("userId", Integer.class));
            request.setAttribute("username", claims.getSubject());
            request.setAttribute("userRole", claims.get("role", String.class));
            filterChain.doFilter(request, response);
        } catch (JwtException e) {
            writeUnauthorized(response, "Token无效或已过期");
        }
    }

    private void writeUnauthorized(HttpServletResponse response, String message) throws IOException {
        response.setStatus(HttpServletResponse.SC_OK);
        response.setContentType("application/json;charset=UTF-8");
        ApiResponse<?> apiResponse = ApiResponse.error(401, message);
        response.getWriter().write(objectMapper.writeValueAsString(apiResponse));
    }
}
