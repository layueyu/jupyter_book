# spring boot 二维码

#### 引入 依赖

```xml
<!-- 二维码支持包 -->
<dependency>
    <groupId>com.google.zxing</groupId>
    <artifactId>core</artifactId>
    <version>3.3.3</version>
</dependency>

<dependency>
    <groupId>net.glxn</groupId>
    <artifactId>qrgen</artifactId>
    <version>1.4</version>
</dependency>
```

#### 工具类

```java
import com.google.zxing.*;
import com.google.zxing.client.j2se.BufferedImageLuminanceSource;
import com.google.zxing.common.BitMatrix;
import com.google.zxing.common.HybridBinarizer;
import com.google.zxing.qrcode.decoder.ErrorCorrectionLevel;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Component;

import javax.imageio.ImageIO;
import java.awt.*;
import java.awt.image.BufferedImage;
import java.io.File;
import java.io.IOException;
import java.util.*;
import java.util.List;

/**
 * 二维码 工具类
 *
 */

@Component
public class QRCodeUtil {

    private Logger logger = LoggerFactory.getLogger(QRCodeUtil.class);

    // 二维码颜色==黑色
    private int BLACK = 0xFF000000;
    // 二维码颜色==白色
    private int WHITE = 0xFFFFFFFF;

    // 二维码图片格式==jpg和png两种
    private  List<String> IMAGE_TYPE = new ArrayList<>();

    public QRCodeUtil() {
        IMAGE_TYPE.add("jpg");
        IMAGE_TYPE.add("png");
    }

    /**
     * 生成二维码，存放在指定的目录
     * @param content 二维码包含的内容，文本或网址
     * @param path 生成的二维码图片存放位置
     * @param size 生成的二维码图片的尺寸，可以自定义或者默认（250）
     * @param logoPath logo的存放位置
     * @return 执行结果
     */
    public  boolean zxingCodeCreate(String content, String path, Integer size, String logoPath) {
        try {
            //图片类型
            String imageType = "jpg";
            //获取二维码流的形式，写入到目录文件中
            BufferedImage image = getBufferedImage(content, size, logoPath);
            //获得随机数
            Random random = new Random();
            // 生成二维码存放文件
            File file = new File(path+random.nextInt(1000)+".jpg");

            // 目录不存在，创建目录
            if (!file.exists()) { file.mkdirs(); }

            ImageIO.write(image, imageType, file);
            return true;
        } catch (IOException e) {
            logger.error("生成二维码：失败===》:{}",e.toString());
            return false;
        }
    }

    /**
     * 二维码流的形式，包含文本内容
     * @param content 二维码文本内容
     * @param size 二维码尺寸
     * @param logoPath logo的存放位置
     * @return
     */
    public  BufferedImage getBufferedImage(String content, Integer size, String logoPath) {
        if (size == null || size <= 0) { size = 250; }

        BufferedImage image = null;

        try {
            // 设置编码字符集
            Map<EncodeHintType, Object> hints = new HashMap<>();

            //设置编码
            hints.put(EncodeHintType.CHARACTER_SET, "UTF-8");

            //设置容错率最高
            hints.put(EncodeHintType.ERROR_CORRECTION, ErrorCorrectionLevel.H);
            hints.put(EncodeHintType.MARGIN, 1);

            // 1、生成二维码
            MultiFormatWriter multiFormatWriter = new MultiFormatWriter();
            BitMatrix bitMatrix = multiFormatWriter.encode(content, BarcodeFormat.QR_CODE, size, size, hints);

            // 2、获取二维码宽高
             int codeWidth = bitMatrix.getWidth();
             int codeHeight = bitMatrix.getHeight();

            // 3、将二维码放入缓冲流
             image = new BufferedImage(codeWidth, codeHeight, BufferedImage.TYPE_INT_RGB);
             for (int i = 0; i < codeWidth; i++) {
                 for (int j = 0; j < codeHeight; j++) {
                     //4、循环将二维码内容定入图片
                     image.setRGB(i, j, bitMatrix.get(i, j) ? BLACK : WHITE);
                 }
             }

            // 判断是否写入logo图片
             if (logoPath != null && !"".equals(logoPath)) {
                 File logoPic = new File(logoPath);
                 if (logoPic.exists()) {
                 Graphics2D g = image.createGraphics();
                 BufferedImage logo = ImageIO.read(logoPic);
                 int widthLogo = logo.getWidth(null) > image.getWidth() * 2 / 10 ? (image.getWidth() * 2 / 10) : logo.getWidth(null);
                 int heightLogo = logo.getHeight(null) > image.getHeight() * 2 / 10 ? (image.getHeight() * 2 / 10) : logo.getHeight(null);
                 int x = (image.getWidth() - widthLogo) / 2; int y = (image.getHeight() - heightLogo) / 2;

                 // 开始绘制图片
                 g.drawImage(logo, x, y, widthLogo, heightLogo, null);
                 g.drawRoundRect(x, y, widthLogo, heightLogo, 15, 15);
                 // 边框宽度
                 g.setStroke(new BasicStroke(2));
                 // 边框颜色
                 g.setColor(Color.WHITE);
                 g.drawRect(x, y, widthLogo, heightLogo);
                 g.dispose(); logo.flush(); image.flush();
                 }
             }
        } catch (WriterException e) {
            logger.error("生成二维码-二进制流：失败===》:{}",e.toString());
        } catch (IOException e) {
            logger.error("生成二维码-二进制流：失败===》:{}",e.toString());
        }
        return image;
    }

    /**
     *  给二维码图片添加Logo
     *  @param qrPic 二维码图片
     *  @param logoPic logo图片
     *  @param path 合成后的图片存储目录
     */
    public  boolean zxingCodeCreate(File qrPic, File logoPic, String path) {
        try {
            String imageType = path.substring(path.lastIndexOf(".") + 1).toLowerCase();
            if (!IMAGE_TYPE.contains(imageType)) { return false; }
            if (!qrPic.isFile() && !logoPic.isFile()) { return false; }

            //读取二维码图片，并构建绘图对象
             BufferedImage image = ImageIO.read(qrPic);
             Graphics2D g = image.createGraphics();
            // 读取Logo图片
             BufferedImage logo = ImageIO.read(logoPic);
            // 设置logo的大小,最多20%0
            int widthLogo = logo.getWidth(null) > image.getWidth() * 2 / 10 ? (image.getWidth() * 2 / 10) : logo.getWidth(null);
            int heightLogo = logo.getHeight(null) > image.getHeight() * 2 / 10 ? (image.getHeight() * 2 / 10) : logo.getHeight(null);
            // 计算图片放置位置，默认在中间
            int x = (image.getWidth() - widthLogo) / 2;
            int y = (image.getHeight() - heightLogo) / 2;
            // 开始绘制图片
            g.drawImage(logo, x, y, widthLogo, heightLogo, null); g.drawRoundRect(x, y, widthLogo, heightLogo, 15, 15);
            // 边框宽度
            g.setStroke(new BasicStroke(2));
            // 边框颜色
            g.setColor(Color.WHITE);
            g.drawRect(x, y, widthLogo, heightLogo);
            g.dispose();
            logo.flush();
            image.flush();
            File newFile = new File(path);
            if (!newFile.exists()) { newFile.mkdirs(); }
            ImageIO.write(image, imageType, newFile);
            return true;
        } catch (Exception e) {
            logger.error("给二维码图片添加Logo：失败===》:{}",e.toString());
            return false;
        }
    }

    /**
     *  二维码的解析方法
     *  @param path 二维码图片目录
     *  @return
     */
    public Result zxingCodeAnalyze(String path) {
        try {
            MultiFormatReader formatReader = new MultiFormatReader();
            File file = new File(path);
            if (file.exists()) {
                BufferedImage image = ImageIO.read(file);
                LuminanceSource source = new BufferedImageLuminanceSource(image);
                Binarizer binarizer = new HybridBinarizer(source);
                BinaryBitmap binaryBitmap = new BinaryBitmap(binarizer);
                Map hints = new HashMap();
                hints.put(EncodeHintType.CHARACTER_SET, "UTF-8");
                Result result = formatReader.decode(binaryBitmap, hints);
                return result;
            }
        } catch (IOException e) {
            logger.error("解析二维码：失败===》:{}",e.toString());
        } catch (NotFoundException e) {
            logger.error("解析二维码：失败===》:{}",e.toString());
        }
        return null;
    }

}
```

#### 使用

```java
package io.renren.modules;

import com.google.zxing.Result;
import io.renren.common.utils.QRCodeUtil;
import io.renren.common.utils.R;
import org.apache.commons.io.IOUtils;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import javax.imageio.ImageIO;
import javax.servlet.ServletOutputStream;
import javax.servlet.http.HttpServletResponse;
import java.awt.image.BufferedImage;
import java.io.IOException;

@RestController
@RequestMapping("/code")
public class QRCodeController {

    @Autowired
    private QRCodeUtil qrCodeUtil;

    /**
     * 生成二维码，保存到本地
     * @return
     */
    @GetMapping("/create")
    public R productcode() {
        boolean b = qrCodeUtil.zxingCodeCreate("http://www.baidu.com", "D:/voice/picture/2018/", 500, "D:/voice/picture/2018/5.jpg");
        return R.ok().put("boolten",b);
    }

    /**
     * 解析二维码
     * @return
     */
    @GetMapping("/test")
    public R analysiscode() {
        Result result = qrCodeUtil.zxingCodeAnalyze("D:/voice/picture/2018/275.jpg");
        System.err.println("二维码解析内容："+result.toString());
        return R.ok().put("result",result);
    }

    /**
     * 生成二维码，通过response返回
     * @param response
     */
    @GetMapping("/test1")
    public void test(HttpServletResponse response) {

        try {
            response.setHeader("Cache-Control", "no-store, no-cache");
            response.setContentType("image/jpeg");

            //获取图片验证码
            BufferedImage image = qrCodeUtil.getBufferedImage("http://www.baidu.com", 500, "D:/voice/picture/2018/5.jpg");

            ServletOutputStream out = response.getOutputStream();
            ImageIO.write(image, "jpg", out);
            IOUtils.closeQuietly(out);
        } catch (IOException e) {
            e.printStackTrace();
        }

    }

}
```



