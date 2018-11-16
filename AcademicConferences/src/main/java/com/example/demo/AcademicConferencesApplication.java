package com.example.demo;

import org.apache.log4j.PropertyConfigurator;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.web.servlet.ServletComponentScan;
import org.springframework.context.annotation.Bean;
import org.springframework.core.task.AsyncTaskExecutor;
import org.springframework.scheduling.annotation.EnableAsync;
import org.springframework.scheduling.concurrent.ThreadPoolTaskExecutor;
import org.springframework.transaction.annotation.EnableTransactionManagement;

import java.net.URL;

@SpringBootApplication
@ServletComponentScan
@EnableTransactionManagement
@EnableAsync
public class AcademicConferencesApplication {

	static
	{
		try
		{
			URL resourcePath=AcademicConferencesApplication.class.getClassLoader().getResource("");
			if(resourcePath == null)
			{
				throw new NullPointerException();
			}
			String log4jPath=resourcePath.getPath()+"/log4j.properties";
			PropertyConfigurator.configure(log4jPath);
		}
		catch (Exception e)
		{
			e.printStackTrace();
		}
	}

	@Bean
	public AsyncTaskExecutor asyncServiceExecutor() {
		ThreadPoolTaskExecutor executor = new ThreadPoolTaskExecutor();
		executor.setThreadNamePrefix("Anno-Executor");
		executor.setMaxPoolSize(10);
        executor.initialize();
		return executor;
	}
	public static void main(String[] args) {
		SpringApplication.run(AcademicConferencesApplication.class, args);
	}
}
