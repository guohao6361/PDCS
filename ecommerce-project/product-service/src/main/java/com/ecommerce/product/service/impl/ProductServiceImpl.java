package com.ecommerce.product.service.impl;

import com.ecommerce.common.BusinessException;
import com.ecommerce.common.PageResponse;
import com.ecommerce.product.entity.Product;
import com.ecommerce.product.entity.Review;
import com.ecommerce.product.repository.ProductRepository;
import com.ecommerce.product.repository.ReviewRepository;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.CommandLineRunner;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Sort;
import org.springframework.data.mongodb.core.MongoTemplate;
import org.springframework.data.mongodb.core.query.Criteria;
import org.springframework.data.mongodb.core.query.Query;
import org.springframework.data.mongodb.core.query.Update;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;
import java.io.IOException;
import java.math.BigDecimal;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.nio.file.StandardOpenOption;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

@Service
public class ProductServiceImpl implements CommandLineRunner {

    private static final Logger log = LoggerFactory.getLogger(ProductServiceImpl.class);

    @Autowired
    private ProductRepository productRepository;

    @Autowired
    private ReviewRepository reviewRepository;

    @Autowired
    private MongoTemplate mongoTemplate;

    @Value("${app.product.default-size:10}")
    private int defaultPageSize;

    @Value("${app.upload.products-dir:uploads/products}")
    private String productsDir;

    // 获取商品列表（分页）
    public PageResponse<Product> getAllProducts(int page, int size) {
        if (size <= 0) size = defaultPageSize;
        PageRequest pageRequest = PageRequest.of(page, size, Sort.by("id").ascending());
        Page<Product> pageResult = productRepository.findAll(pageRequest);
        return new PageResponse<>(pageResult.getContent(), page, size, (int) pageResult.getTotalElements());
    }

    // 搜索商品（按名称或分类）
    public PageResponse<Product> searchProducts(String keyword, int page, int size) {
        if (size <= 0) size = defaultPageSize;
        PageRequest pageRequest = PageRequest.of(page, size, Sort.by("id").ascending());
        Page<Product> pageResult = productRepository.searchByNameOrCategory(keyword, pageRequest);
        return new PageResponse<>(pageResult.getContent(), page, size, (int) pageResult.getTotalElements());
    }

    // 获取单件商品详情
    public Product getProduct(Integer id) {
        return productRepository.findById(id)
                .orElseThrow(() -> new BusinessException(404, "商品不存在"));
    }

    // 发表评价
    public Review addReview(Review review) {
        return reviewRepository.save(review);
    }

    // 查询某商品的所有评价
    public List<Review> getReviews(Integer productId) {
        return reviewRepository.findByProductId(productId);
    }

    // 原子扣减库存（防止超卖）
    public void deductStock(Integer productId, Integer quantity) {
        Query query = new Query(Criteria.where("_id").is(productId)
                .and("stock").gte(quantity));
        Update update = new Update().inc("stock", -quantity);
        var result = mongoTemplate.updateFirst(query, update, Product.class);
        if (result.getModifiedCount() == 0) {
            throw new BusinessException(400, "商品库存不足或商品不存在: " + productId);
        }
        log.info("库存扣减成功: productId={}, quantity={}", productId, quantity);
    }

    // 原子恢复库存
    public void restoreStock(Integer productId, Integer quantity) {
        Query query = new Query(Criteria.where("_id").is(productId));
        Update update = new Update().inc("stock", quantity);
        var result = mongoTemplate.updateFirst(query, update, Product.class);
        if (result.getModifiedCount() == 0) {
            throw new BusinessException(404, "商品不存在: " + productId);
        }
        log.info("库存恢复成功: productId={}, quantity={}", productId, quantity);
    }

    private static final List<String> ALLOWED_IMAGE_TYPES = List.of("image/jpeg", "image/png", "image/gif", "image/webp");

    // 上传商品图片
    public String uploadProductImage(byte[] fileData, String originalFilename) {
        return uploadProductImage(fileData, originalFilename, null);
    }

    public String uploadProductImage(byte[] fileData, String originalFilename, String contentType) {
        // 安全修复: 文件类型校验
        if (contentType != null && !ALLOWED_IMAGE_TYPES.contains(contentType.toLowerCase())) {
            throw new BusinessException(400, "仅支持 JPG/PNG/GIF/WebP 图片格式");
        }
        try {
            Path dir = Paths.get(productsDir);
            Files.createDirectories(dir);
            String ext = originalFilename != null && originalFilename.contains(".")
                    ? originalFilename.substring(originalFilename.lastIndexOf("."))
                    : ".jpg";
            String filename = "product_" + System.currentTimeMillis() + ext;
            Path filePath = dir.resolve(filename);
            Files.write(filePath, fileData, StandardOpenOption.CREATE, StandardOpenOption.TRUNCATE_EXISTING);
            String imageUrl = "/uploads/products/" + filename;
            log.info("商品图片上传成功: url={}", imageUrl);
            return imageUrl;
        } catch (IOException e) {
            log.error("商品图片上传失败: {}", e.getMessage());
            throw new BusinessException(500, "图片上传失败");
        }
    }

    // 商家发布商品
    public Product createProduct(Product product) {
        return productRepository.save(product);
    }

    // 商家修改商品
    public Product updateProduct(Integer id, Product updates) {
        Product product = productRepository.findById(id)
                .orElseThrow(() -> new BusinessException(404, "商品不存在"));
        if (updates.getName() != null) product.setName(updates.getName());
        if (updates.getPrice() != null) product.setPrice(updates.getPrice());
        if (updates.getStock() != null) product.setStock(updates.getStock());
        if (updates.getCategory() != null) product.setCategory(updates.getCategory());
        if (updates.getDescription() != null) product.setDescription(updates.getDescription());
        if (updates.getImageUrl() != null) product.setImageUrl(updates.getImageUrl());
        return productRepository.save(product);
    }

    // 商家删除商品
    public void deleteProduct(Integer id) {
        if (!productRepository.existsById(id)) {
            throw new BusinessException(404, "商品不存在");
        }
        productRepository.deleteById(id);
        log.info("商品删除成功: productId={}", id);
    }

    // 商家商品列表
    public List<Product> getProductsByMerchant(Integer merchantId) {
        return productRepository.findByMerchantId(merchantId);
    }

    // ==========================================================
    // 自动初始化 MongoDB 实验数据 [1.1.2]
    // ==========================================================
    @Override
    public void run(String... args) throws Exception {
        if (productRepository.count() == 0) {
            // 1. 初始化华为 Mate 60 (带手机特有动态属性) [1.1.2]
            Product p1 = new Product();
            p1.setId(1);
            p1.setName("华为 Mate 60");
            p1.setPrice(new BigDecimal("6999.00"));
            p1.setStock(50);
            p1.setCategory("Electronics");
            Map<String, Object> attr1 = new HashMap<>();
            attr1.put("color", "雅川青");
            attr1.put("storage", "512GB");
            attr1.put("network", "5G");
            p1.setAttributes(attr1);
            productRepository.save(p1);

            // 2. 初始化机械键盘 (带键盘特有动态属性) [1.1.2]
            Product p2 = new Product();
            p2.setId(2);
            p2.setName("机械键盘");
            p2.setPrice(new BigDecimal("499.00"));
            p2.setStock(100);
            p2.setCategory("Accessories");
            Map<String, Object> attr2 = new HashMap<>();
            attr2.put("switchType", "红轴");
            attr2.put("backlight", "RGB");
            p2.setAttributes(attr2);
            productRepository.save(p2);

            // 3. 初始化降噪耳机 (带耳机特有动态属性) [1.1.2]
            Product p3 = new Product();
            p3.setId(3);
            p3.setName("降噪耳机");
            p3.setPrice(new BigDecimal("1299.00"));
            p3.setStock(30);
            p3.setCategory("Accessories");
            Map<String, Object> attr3 = new HashMap<>();
            attr3.put("ancDepth", "40dB");
            attr3.put("batteryLife", "30h");
            p3.setAttributes(attr3);
            productRepository.save(p3);

            log.info("MongoDB 商品实验数据初始化成功");
        }
    }
}