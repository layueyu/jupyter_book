# springboot 文件上传

### 使用FTP

- 引用依赖jar包

  ```xml
   <dependency>
       <groupId>commons-net</groupId>
       <artifactId>commons-net</artifactId>
       <version>3.6</version>
  </dependency>
  <dependency>
      <groupId>org.apache.commons</groupId>
      <artifactId>commons-pool2</artifactId>
      <version>2.6.0</version>
  </dependency>
  ```


- 编写配置实体,FtpConfigProperties.java

  ```java
  package io.renren.config.ftppool.entity;
  
  import org.springframework.beans.factory.annotation.Value;
  import org.springframework.stereotype.Component;
  
  /**
   * FTP 配置读取类
   * 从配置文件读取FTP配置
   * 配置信息前缀：renren.file.ftp
   */
  @Component
  public class FtpConfigProperties {
      /*FTP 主机地址*/
      @Value("${renren.file.ftp.host:localhost}")
      private String host;
      /*FTP 端口号*/
      @Value("${renren.file.ftp.port:21}")
      private int port;
      /*用户名*/
      @Value("${renren.file.ftp.username}")
      private String username;
      /*密码*/
      @Value("${renren.file.ftp.passowrd}")
      private String passowrd;
      /*缓存大小*/
      private int bufferSize = 8096;
      /*初始化连接数*/
      @Value("${renren.file.ftp.initialSzie:0}")
      private Integer initialSzie;
      /*编码*/
      @Value("${renren.file.ftp.encoding:UTF-8}")
      private String encoding;
      /*启用被动模式*/
      @Value("${renren.file.ftp.enterLocalPassiveMode:true}")
      private boolean enterLocalPassiveMode;
  
      public String getHost() {
          return host;
      }
  
      public void setHost(String host) {
          this.host = host;
      }
  
      public int getPort() {
          return port;
      }
  
      public void setPort(int port) {
          this.port = port;
      }
  
      public String getUsername() {
          return username;
      }
  
      public void setUsername(String username) {
          this.username = username;
      }
  
      public String getPassowrd() {
          return passowrd;
      }
  
      public void setPassowrd(String passowrd) {
          this.passowrd = passowrd;
      }
  
      public int getBufferSize() {
          return bufferSize;
      }
  
      public void setBufferSize(int bufferSize) {
          this.bufferSize = bufferSize;
      }
  
      public Integer getInitialSzie() {
          return initialSzie;
      }
  
      public void setInitialSzie(Integer initialSzie) {
          this.initialSzie = initialSzie;
      }
  
      public String getEncoding() {
          return encoding;
      }
  
      public void setEncoding(String encoding) {
          this.encoding = encoding;
      }
  
      public boolean isEnterLocalPassiveMode() {
          return enterLocalPassiveMode;
      }
  
      public void setEnterLocalPassiveMode(boolean enterLocalPassiveMode) {
          this.enterLocalPassiveMode = enterLocalPassiveMode;
      }
  }
  
  ```

- 编写配置信息，【yml】

  ```yml
  renren:
    file:
      rootPath: rootPath # 上传文件根路径
      httpServerUri: localhost:8080 #文件服务器地址
      mode: ftp # 上传方式 ftp：使用FTP上传 local：上传到项目所在路径
      ftp:
        isopen: true # 开启FTP配置类
        host: localhost #FTP 服务器地址
        port: 21 # FTP 端口号
        username: admin # FTP 用户名
        passowrd: admin # FTP 密码
        initialSzie: 0 # 初始连接数
        enterLocalPassiveMode: false # 启用被动模式
  ```

- 编写FTP服务类，FtpModel.java

  ```java
  package io.renren.config.ftppool.entity;
  
  
  import cn.hutool.core.util.ArrayUtil;
  import cn.hutool.core.util.StrUtil;
  import org.apache.commons.net.ftp.FTPClient;
  import org.apache.commons.net.ftp.FTPFile;
  import org.apache.commons.pool2.ObjectPool;
  import org.slf4j.Logger;
  import org.slf4j.LoggerFactory;
  import org.springframework.util.Assert;
  
  import java.io.*;
  import java.util.ArrayList;
  import java.util.Arrays;
  import java.util.List;
  import java.util.Objects;
  import java.util.stream.Collectors;
  
  /**
   * FTP 服务
   */
  public class FtpModel {
  
      private Logger log = LoggerFactory.getLogger(this.getClass());
  
      /**
       * 是否使用被动模式设置
       */
      private boolean enterLocalPassiveMode = true;
      /**
       * ftpClient连接池初始化标志
       */
      private boolean hasInit = false;
      /**
       * ftpClient连接池
       */
      private ObjectPool<FTPClient> ftpClientPool;
  
      public boolean isHasInit() {
          return hasInit;
      }
  
      public void setHasInit(boolean hasInit) {
          this.hasInit = hasInit;
      }
  
      public ObjectPool<FTPClient> getFtpClientPool() {
          return ftpClientPool;
      }
  
      public void setFtpClientPool(ObjectPool<FTPClient> ftpClientPool) {
          this.ftpClientPool = ftpClientPool;
      }
  
      public boolean isEnterLocalPassiveMode() {
          return enterLocalPassiveMode;
      }
  
      public void setEnterLocalPassiveMode(boolean enterLocalPassiveMode) {
          this.enterLocalPassiveMode = enterLocalPassiveMode;
      }
  
      /**
       * 上传文件
       * @param pathname ftp服务保存地址
       * @param fileName 上传到ftp的文件名
       *  @param originfilename 待上传文件的名称（绝对地址） *
       * @return
       */
      public boolean uploadFile( String pathname, String fileName,String originfilename){
          boolean flag = false;
          InputStream inputStream = null;
          FTPClient ftpClient = getFtpClient();
          try{
              log.info("开始上传文件");
              inputStream = new FileInputStream(new File(originfilename));
              ftpClient.setFileType(ftpClient.BINARY_FILE_TYPE);
              if(CreateDirecroty(pathname,ftpClient)){
                  ftpClient.changeWorkingDirectory(pathname);
                  ftpClient.storeFile(fileName, inputStream);
                  inputStream.close();
                  flag = true;
                  log.info("上传文件成功");
              }else {
                  flag = false;
                  log.info("上传文件失败");
              }
          }catch (Exception e) {
              log.error("上传文件失败");
              e.printStackTrace();
          }finally{
              releaseFtpClient(ftpClient);
          }
          return flag;
      }
  
      /**
       * 上传文件
       * @param pathname ftp服务保存地址
       * @param fileName 上传到ftp的文件名
       * @param inputStream 输入文件流
       * @return
       */
      public boolean uploadFile( String pathname, String fileName,InputStream inputStream){
          boolean flag = false;
          FTPClient ftpClient = getFtpClient();
          try{
              log.info("开始上传文件");
              ftpClient.setFileType(ftpClient.BINARY_FILE_TYPE);
              if(CreateDirecroty(pathname,ftpClient)){
                  ftpClient.changeWorkingDirectory(pathname);
                  ftpClient.storeFile(fileName, inputStream);
                  inputStream.close();
                  flag = true;
                  log.info("上传文件成功");
              }else {
                  flag = true;
                  log.info("上传文失败");
              }
          }catch (Exception e) {
              log.error("上传文件失败");
              e.printStackTrace();
          }finally{
              releaseFtpClient(ftpClient);
          }
          return flag;
      }
  
      /** * 下载文件 *
       * @param pathname FTP服务器文件目录 *
       * @param filename 文件名称 *
       * @param localpath 下载后的文件路径 *
       * @return */
      public  boolean downloadFile(String pathname, String filename, String localpath){
          boolean flag = false;
          OutputStream os=null;
          FTPClient ftpClient = getFtpClient();
          try {
              log.info("开始下载文件");
              //切换FTP目录
              ftpClient.changeWorkingDirectory(pathname);
              FTPFile[] ftpFiles = ftpClient.listFiles();
              for(FTPFile file : ftpFiles){
                  if(filename.equalsIgnoreCase(file.getName())){
                      File localFile = new File(localpath + "/" + file.getName());
                      os = new FileOutputStream(localFile);
                      ftpClient.retrieveFile(file.getName(), os);
                      os.close();
                  }
              }
              flag = true;
              log.info("下载文件成功");
          } catch (Exception e) {
              log.error("下载文件失败");
              e.printStackTrace();
          } finally{
              releaseFtpClient(ftpClient);
              if(null != os){
                  try {
                      os.close();
                  } catch (IOException e) {
                      e.printStackTrace();
                  }
              }
          }
          return flag;
      }
  
      /** * 删除文件 *
       * @param pathname FTP服务器保存目录 *
       * @param filename 要删除的文件名称 *
       * @return */
      public boolean deleteFile(String pathname, String filename){
          boolean flag = false;
          FTPClient ftpClient = getFtpClient();
          try {
              log.info("开始删除文件");
              //切换FTP目录
              ftpClient.changeWorkingDirectory(pathname);
              ftpClient.dele(filename);
              ftpClient.logout();
              flag = true;
              log.info("删除文件成功");
          } catch (Exception e) {
              log.error("删除文件失败");
              e.printStackTrace();
          } finally {
              releaseFtpClient(ftpClient);
          }
          return flag;
      }
  
      /**
       * 按行读取FTP文件
       *
       * @param remoteFilePath 文件路径（path+fileName）
       * @return
       * @throws IOException
       */
      public List<String> readFileByLine(String remoteFilePath) throws IOException {
          FTPClient ftpClient = getFtpClient();
          try (InputStream in = ftpClient.retrieveFileStream(encodingPath(remoteFilePath));
               BufferedReader br = new BufferedReader(new InputStreamReader(in))) {
              return br.lines().map(line -> StrUtil.trimToEmpty(line))
                      .filter(line -> StrUtil.isNotEmpty(line)).collect(Collectors.toList());
          } finally {
              ftpClient.completePendingCommand();
              releaseFtpClient(ftpClient);
          }
      }
  
      /**
       * 获取指定路径下FTP文件
       *
       * @param remotePath 路径
       * @return FTPFile数组
       * @throws IOException
       */
      public FTPFile[] retrieveFTPFiles(String remotePath) throws IOException {
          FTPClient ftpClient = getFtpClient();
          try {
              return ftpClient.listFiles(encodingPath(remotePath + "/"),
                      file -> file != null && file.getSize() > 0);
          } finally {
              releaseFtpClient(ftpClient);
          }
      }
  
      /**
       * 获取指定路径下FTP文件名称
       *
       * @param remotePath 路径
       * @return ftp文件名称列表
       * @throws IOException
       */
      public List<String> retrieveFileNames(String remotePath) throws IOException {
          FTPFile[] ftpFiles = retrieveFTPFiles(remotePath);
          if (ArrayUtil.isEmpty(ftpFiles)) {
              return new ArrayList<>();
          }
          return Arrays.stream(ftpFiles).filter(Objects::nonNull)
                  .map(FTPFile::getName).collect(Collectors.toList());
      }
  
      /**
       * 编码文件路径
       */
      private static String encodingPath(String path) throws UnsupportedEncodingException {
          // FTP协议里面，规定文件名编码为iso-8859-1，所以目录名或文件名需要转码
          return new String(path.replaceAll("//", "/").getBytes("GBK"), "iso-8859-1");
      }
  
      /**
       * 获取ftpClient
       *
       * @return
       */
      private FTPClient getFtpClient() {
          checkFtpClientPoolAvailable();
          FTPClient ftpClient = null;
          Exception ex = null;
          // 获取连接最多尝试3次
          for (int i = 0; i < 3; i++) {
              try {
                  ftpClient = ftpClientPool.borrowObject();
                  if(enterLocalPassiveMode) {
                      ftpClient.enterLocalPassiveMode();//被动模式
                  }
                  ftpClient.changeWorkingDirectory("/");
                  break;
              } catch (Exception e) {
                  ex = e;
              }
          }
          if (ftpClient == null) {
              throw new RuntimeException("Could not get a ftpClient from the pool", ex);
          }
          return ftpClient;
      }
  
      /**
       * 释放ftpClient
       */
      private void releaseFtpClient(FTPClient ftpClient) {
          if (ftpClient == null) {
              return;
          }
  
          try {
              ftpClientPool.returnObject(ftpClient);
          } catch (Exception e) {
              log.error("Could not return the ftpClient to the pool", e);
              // destoryFtpClient
              if (ftpClient.isAvailable()) {
                  try {
                      ftpClient.disconnect();
                  } catch (IOException io) {
                  }
              }
          }
      }
  
      /**
       * 检查ftpClientPool是否可用
       */
      private void checkFtpClientPoolAvailable() {
          Assert.state(hasInit, "FTP未启用或连接失败！");
      }
  
  
      /**
       * 创建多层目录文件，如果有ftp服务器已存在该文件，则不创建，如果无，则创建
       * @param remote
       * @param ftpClient
       * @return
       * @throws IOException
       */
      public boolean CreateDirecroty(String remote,FTPClient ftpClient) throws IOException {
          boolean success = true;
          String directory = remote + "/";
          // 如果远程目录不存在，则递归创建远程服务器目录
          if (!directory.equalsIgnoreCase("/") && !changeWorkingDirectory(new String(directory),ftpClient)) {
              int start = 0;
              int end = 0;
              if (directory.startsWith("/")) {
                  start = 1;
              } else {
                  start = 0;
              }
              end = directory.indexOf("/", start);
              String path = "";
              String paths = "";
              while (true) {
                  String subDirectory = new String(remote.substring(start, end).getBytes("GBK"), "iso-8859-1");
                  path = path + "/" + subDirectory;
                  if (!existFile(path,ftpClient)) {
                      if (makeDirectory(subDirectory,ftpClient)) {
                          changeWorkingDirectory(subDirectory,ftpClient);
                      } else {
                          log.error("创建目录[{}]失败",subDirectory);
                          changeWorkingDirectory(subDirectory,ftpClient);
                      }
                  } else {
                      changeWorkingDirectory(subDirectory,ftpClient);
                  }
  
                  paths = paths + "/" + subDirectory;
                  start = end + 1;
                  end = directory.indexOf("/", start);
                  // 检查所有目录是否创建完毕
                  if (end <= start) {
                      break;
                  }
              }
          }
          return success;
      }
  
      /**
       * 改变目录路径
       * @param directory
       * @param ftpClient
       * @return
       */
      public boolean changeWorkingDirectory(String directory,FTPClient ftpClient) {
          boolean flag = true;
          try {
              flag = ftpClient.changeWorkingDirectory(directory);
              if (flag) {
                  log.info("进入目录[{}]成功！",directory);
  
              } else {
                  log.info("进入目录[{}]失败！开始创建目录");
              }
          } catch (IOException ioe) {
              ioe.printStackTrace();
          }
          return flag;
      }
  
      //判断ftp服务器文件是否存在
      public boolean existFile(String path,FTPClient ftpClient) throws IOException {
          boolean flag = false;
          FTPFile[] ftpFileArr = ftpClient.listFiles(path);
          if (ftpFileArr.length > 0) {
              flag = true;
          }
          return flag;
      }
      //创建目录
      public boolean makeDirectory(String dir,FTPClient ftpClient) {
          boolean flag = true;
          try {
              flag = ftpClient.makeDirectory(dir);
              if (flag) {
                  log.info("创建文件夹[{}] 成功！",dir);
  
              } else {
                  log.info("创建文件夹[{}] 失败！",dir);
              }
          } catch (Exception e) {
              e.printStackTrace();
          }
          return flag;
      }
  }
  ```

- 编写配置类，FtpConfiguration.java

  ```java
  package io.renren.config.ftppool;
  
  import io.renren.config.ftppool.entity.FtpConfigProperties;
  import io.renren.config.ftppool.entity.FtpModel;
  import org.apache.commons.net.ftp.FTPClient;
  import org.apache.commons.pool2.ObjectPool;
  import org.apache.commons.pool2.PooledObject;
  import org.apache.commons.pool2.PooledObjectFactory;
  import org.apache.commons.pool2.impl.DefaultPooledObject;
  import org.apache.commons.pool2.impl.GenericObjectPool;
  import org.apache.commons.pool2.impl.GenericObjectPoolConfig;
  import org.slf4j.Logger;
  import org.slf4j.LoggerFactory;
  import org.springframework.beans.factory.annotation.Autowired;
  import org.springframework.boot.autoconfigure.condition.ConditionalOnClass;
  import org.springframework.boot.autoconfigure.condition.ConditionalOnMissingBean;
  import org.springframework.boot.autoconfigure.condition.ConditionalOnProperty;
  import org.springframework.context.annotation.Bean;
  import org.springframework.context.annotation.Configuration;
  
  import javax.annotation.PreDestroy;
  
  /**
   * FTP 配置类
   */
  @Configuration //开启配置
  @ConditionalOnClass({FtpModel.class, GenericObjectPool.class, FTPClient.class})//存在FtpModel时初始化该配置类
  @ConditionalOnProperty//存在对应配置信息时初始化该配置类
          (
                  prefix = "renren.file.ftp", //配置前缀
                  name = "isopen",
                  havingValue = "true",   //开启
                  matchIfMissing = true   //缺失检查
          )
  public class FtpConfiguration {
      //获取日志
      private Logger log = LoggerFactory.getLogger(this.getClass());
  
      @Autowired
      private FtpConfigProperties ftpConfigProperties;
  
      /*连接池*/
      private ObjectPool<FTPClient> pool;
  
      /**
       * 预先加载FTPClient连接到对象池中
       * @param initialSize 初始化连接数
       * @param maxIdle 最大空闲连接数
       */
      private void preLoadingFtpClient(Integer initialSize, int maxIdle) {
          if (initialSize == null || initialSize <= 0) {
              return;
          }
          int size = Math.min(initialSize.intValue(), maxIdle);
          for (int i = 0; i < size; i++) {
              try {
                  pool.addObject();
              } catch (Exception e) {
                  log.error("预先加载FTPClient异常(preLoadingFtpClient error)...", e);
              }
          }
      }
  
      /**
       * 销毁FTP客户端连接池
       */
      @PreDestroy
      public void destroy() {
          if (pool != null) {
              pool.close();
              log.info("销毁FtpClientPool...");
          }
      }
  
      @Bean//创建FtpModel实体bean
      @ConditionalOnMissingBean(FtpModel.class)//缺失FtpModel实体bean时，初始化FtpModel并添加到SpringIoc
      public FtpModel ftpModel()
              throws Exception{
          log.info(">>>没有发现FtpModel实体Bean，将创建一个新的Bean(The FtpModel Not Found，Execute Creat New Bean.");
          GenericObjectPoolConfig poolConfig = new GenericObjectPoolConfig();
          poolConfig.setTestOnBorrow(true);
          poolConfig.setTestOnReturn(true);
          poolConfig.setTestWhileIdle(true);
          poolConfig.setMinEvictableIdleTimeMillis(60000);
          poolConfig.setSoftMinEvictableIdleTimeMillis(50000);
          poolConfig.setTimeBetweenEvictionRunsMillis(30000);
          pool = new GenericObjectPool<>(new FtpClientPooledObjectFactory(ftpConfigProperties), poolConfig);
          preLoadingFtpClient(ftpConfigProperties.getInitialSzie(), poolConfig.getMaxIdle());
          FtpModel ftpModel =new FtpModel();
          ftpModel.setFtpClientPool(pool);
          ftpModel.setHasInit(true);
          ftpModel.setEnterLocalPassiveMode(ftpConfigProperties.isEnterLocalPassiveMode());
          return ftpModel;
      }
  
      /**
       * FtpClient对象工厂类
       */
      static class FtpClientPooledObjectFactory implements PooledObjectFactory<FTPClient> {
          private Logger log = LoggerFactory.getLogger(this.getClass());
  
          private FtpConfigProperties props;
  
          public FtpClientPooledObjectFactory(FtpConfigProperties props) {
              this.props = props;
          }
  
          @Override
          public PooledObject<FTPClient> makeObject() throws Exception {
              FTPClient ftpClient = new FTPClient();
              try {
                  ftpClient.connect(props.getHost(), props.getPort());
                  ftpClient.login(props.getUsername(), props.getPassowrd());
                  log.info("连接FTP服务器返回码{}", ftpClient.getReplyCode());
                  ftpClient.setBufferSize(props.getBufferSize());
                  ftpClient.setControlEncoding(props.getEncoding());
                  ftpClient.setFileType(FTPClient.BINARY_FILE_TYPE);
                  ftpClient.enterLocalPassiveMode();
                  return new DefaultPooledObject<>(ftpClient);
              } catch (Exception e) {
                  log.error("建立FTP连接失败", e);
                  if (ftpClient.isAvailable()) {
                      ftpClient.disconnect();
                  }
                  ftpClient = null;
                  throw new Exception("建立FTP连接失败", e);
              }
          }
          @Override
          public void destroyObject(PooledObject<FTPClient> p) throws Exception {
              FTPClient ftpClient = getObject(p);
              if (ftpClient != null && ftpClient.isConnected()) {
                  ftpClient.disconnect();
              }
          }
  
          @Override
          public boolean validateObject(PooledObject<FTPClient> p) {
              FTPClient ftpClient = getObject(p);
              if (ftpClient == null || !ftpClient.isConnected()) {
                  return false;
              }
              try {
                  ftpClient.changeWorkingDirectory("/");
                  return true;
              } catch (Exception e) {
                  log.error("验证FTP连接失败::{}",e.getMessage());
                  return false;
              }
          }
  
          @Override
          public void activateObject(PooledObject<FTPClient> p) throws Exception {
          }
  
          @Override
          public void passivateObject(PooledObject<FTPClient> p) throws Exception {
          }
  
          private FTPClient getObject(PooledObject<FTPClient> p) {
              if (p == null || p.getObject() == null) {
                  return null;
              }
              return p.getObject();
          }
  
      }
  }
  ```

- 编写FTP工具类，FtpUtils.java

  ```java
  package io.renren.common.utils;
  
  import io.renren.config.ftppool.entity.FtpModel;
  import org.slf4j.Logger;
  import org.slf4j.LoggerFactory;
  import org.springframework.beans.factory.annotation.Autowired;
  import org.springframework.beans.factory.annotation.Value;
  import org.springframework.stereotype.Component;
  import org.springframework.web.multipart.MultipartFile;
  
  import java.io.InputStream;
  import java.text.DateFormat;
  import java.text.SimpleDateFormat;
  import java.util.*;
  
  /**
   * FTP 工具类
   */
  @Component
  public class FtpUtils {
  
      @Autowired
      private FtpModel ftpModel;
  
      @Value("${renren.file.rootPath:uploadHome}")
      private String rootPath;
  
      @Value("${renren.file.httpServerUri:localhost}")
      private String httpServerUri;
  
      //获取日志
      private Logger log = LoggerFactory.getLogger(this.getClass());
  
      //文件路径集合
      private List<R> filePathList;
  
      public List<R> getFilePathList() {
          return filePathList;
      }
  
      /**
       * 在HTTP请求内获取文件，并上传到FTP
       * @param multipartFile
       * @return
       */
      public R  uploadFile(MultipartFile multipartFile) throws Exception {
          Map<String,Object> result = new HashMap<>();
          if(multipartFile == null){
              log.info("没有获取到上传的文件(No uploaded files were retrieved)");
              return R.error("没有获取到上传的文件(No uploaded files were retrieved)");
          }
          InputStream input = null;
          try {
              //MultipartFile multipartFile = (MultipartFile)file;
              String originFileName = multipartFile.getOriginalFilename();
              //当前上传文件的文件后缀
              String suffix = originFileName.indexOf(".") != -1 ? originFileName.substring(originFileName.lastIndexOf("."),
                      originFileName.length()) : null;
  
              //重命名上传后的文件名
              String uuid = UUID.randomUUID().toString().replaceAll("-", "");
              String saveFileName = uuid + suffix;
  
              //定义上传路径
              DateFormat dataFormat = new SimpleDateFormat("yyyyMMdd");
              String dirPath = rootPath + "/" + dataFormat.format(new Date());
  
              // 获取输入流
              input = multipartFile.getInputStream();
  
              // 上传文件
              boolean b = ftpModel.uploadFile(dirPath, saveFileName, input);
              if(b){
                  return R.ok()
                          .put("filename",originFileName)
                          .put("filePath",httpServerUri+"/"+dirPath+"/"+saveFileName);
              }else {
                  return R.error("上传文件失败");
              }
          }catch (Exception e){
              log.error("上传文件（FtpUtils）异常，{}",e.getLocalizedMessage());
              return R.error("上传文件失败");
          }finally {
              try {
                  if(input != null){
                      input.close();
                  }
              }catch (Exception e){
  
              }
          }
      }
  
  
      /**
       * 多文件文件上传到ftp
       * @param files
       * @return
       */
      public boolean  uploadFileList(MultipartFile[] files) throws Exception {
          if(files == null || files.length == 0 ){return  false;}
          filePathList = new ArrayList<>();
          for(MultipartFile item : files){
              filePathList.add(uploadFile(item));
          }
          return true;
      }
  }
  ```


### 上传到本地

- 编写工具类，

  ```java
  package io.renren.common.utils;
  
  import org.slf4j.Logger;
  import org.slf4j.LoggerFactory;
  import org.springframework.beans.factory.annotation.Value;
  import org.springframework.stereotype.Component;
  import org.springframework.web.multipart.MultipartFile;
  
  import java.io.File;
  import java.text.DateFormat;
  import java.text.SimpleDateFormat;
  import java.util.*;
  
  @Component
  public class FileUtil {
      //ftp服务器ip地址
      @Value("${renren.file.rootPath:uploadHome}")
      private String rootPath;
      @Value("${renren.file.httpServerUri:localhost}")
      private String httpServerUri;
  
      //获取日志
      private Logger log = LoggerFactory.getLogger(this.getClass());
  
      //文件路径集合
      private List<R> filePathList;
  
      public List<R> getFilePathList() {
          return filePathList;
      }
  
      /**
       * 文件上传
       * @param multipartFile
       * @return
       */
      public R uploadFile(MultipartFile multipartFile) {
          if(multipartFile == null){
              return R.error("没有获取到上传的文件");
          }
          try {
              //MultipartFile multipartFile = (MultipartFile)file;
              String originFileName = multipartFile.getOriginalFilename();
              //当前上传文件的文件后缀
              String suffix = originFileName.indexOf(".") != -1 ? originFileName.substring(originFileName.lastIndexOf("."),
                      originFileName.length()) : null;
  
              //重命名上传后的文件名
              String uuid = UUID.randomUUID().toString().replaceAll("-", "");
              String saveFileName = uuid + suffix;
  
              //定义上传路径
              DateFormat dataFormat = new SimpleDateFormat("yyyyMMdd");
              String tmppath = rootPath + "/" + dataFormat.format(new Date()) + "/";
  
              //文件最终保存全路径
              String fileNamePath = tmppath + saveFileName;
  
              //创建File对象
              File localFile = new File(System.getProperty("user.dir")+fileNamePath);
  
              //检测是否存在目录，不存在则创建
              if (!localFile.getParentFile().exists()) {
                  localFile.getParentFile().mkdirs();
              }
              //执行上传文件
              multipartFile.transferTo(localFile);
              return R.ok()
                      .put("filename",originFileName)
                      .put("filepath",httpServerUri+fileNamePath);
          }catch (Exception e){
              log.error("上传文件（FtpUtils）异常，{}",e.getLocalizedMessage());
              return R.error("上传文件失败");
          }
      }
  
      /**
       * 文件上传
       * @param files
       * @return
       */
      public boolean  uploadFileList(MultipartFile[] files) throws Exception {
          if(files == null || files.length == 0 ){return  false;}
          filePathList = new ArrayList<>();
  
          for(MultipartFile item : files){
              filePathList.add(uploadFile(item));
          }
          return true;
      }
  }
  ```

### 使用

- 编写controller类，UploadFileController.java

  ```java
  package io.renren.modules.uploadfile.controller;
  
  import io.renren.common.utils.FileUtil;
  import io.renren.common.utils.FtpUtils;
  import io.renren.common.utils.R;
  import org.springframework.beans.factory.annotation.Autowired;
  import org.springframework.beans.factory.annotation.Value;
  import org.springframework.web.bind.annotation.PostMapping;
  import org.springframework.web.bind.annotation.RequestMapping;
  import org.springframework.web.bind.annotation.RequestParam;
  import org.springframework.web.bind.annotation.RestController;
  import org.springframework.web.multipart.MultipartFile;
  
  @RestController
  @RequestMapping("/file")
  public class UploadFileController {
  
      @Value("${renren.file.mode:local}")
      private  String mode;
  
      @Autowired
      private FileUtil fileUtil;
  
      @Autowired
      private FtpUtils ftpUtils;
  
      @PostMapping("/upload")
      private R upload(@RequestParam("file") MultipartFile[] files){
          try {
              switch (mode){
                  case "local":
                      boolean b = fileUtil.uploadFileList(files);
                      if(b){
                          return R.ok().put("paths", fileUtil.getFilePathList());
                      }
                      break;
                  case "ftp":
                      boolean bb = ftpUtils.uploadFileList(files);
                      if(bb){
                          return R.ok().put("paths", ftpUtils.getFilePathList());
                      }
                      break;
              }
  
          } catch (Exception e) {
  
          }
          return R.error("没有获取到上传文件");
      }
  }
  ```


