package com.ecommerce.user.config;

import com.ecommerce.common.AdminRequired;
import com.ecommerce.common.BusinessException;
import org.springframework.stereotype.Component;
import org.springframework.web.method.HandlerMethod;
import org.springframework.web.servlet.HandlerInterceptor;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;

@Component
public class AdminAuthInterceptor implements HandlerInterceptor {
    
    @Override
    public boolean preHandle(HttpServletRequest request, HttpServletResponse response, Object handler) {
        if (handler instanceof HandlerMethod) {
            HandlerMethod handlerMethod = (HandlerMethod) handler;
            if (handlerMethod.hasMethodAnnotation(AdminRequired.class)) {
                String role = (String) request.getAttribute("userRole");
                if (!"ADMIN".equals(role)) {
                    throw new BusinessException(403, "需要管理员权限");
                }
            }
        }
        return true;
    }
}
