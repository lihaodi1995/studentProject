package model;
// Generated 2017-7-4 19:51:05 by Hibernate Tools 5.2.1.Final

import java.util.Date;

/**
 * Task generated by hbm2java
 */
public class Task implements java.io.Serializable {

	private Integer id;
	private String title;
	private String info;
	private int courseId;
	private Date startTime;
	private Date endTime;
	private byte status;
	private Double weight;

	public Task() {
	}

	public Task(String title, int courseId, byte status) {
		this.title = title;
		this.courseId = courseId;
		this.status = status;
	}

	public Task(String title, String info, int courseId, Date startTime, Date endTime, byte status, Double weight) {
		this.title = title;
		this.info = info;
		this.courseId = courseId;
		this.startTime = startTime;
		this.endTime = endTime;
		this.status = status;
		this.weight = weight;
	}

	public Integer getId() {
		return this.id;
	}

	public void setId(Integer id) {
		this.id = id;
	}

	public String getTitle() {
		return this.title;
	}

	public void setTitle(String title) {
		this.title = title;
	}

	public String getInfo() {
		return this.info;
	}

	public void setInfo(String info) {
		this.info = info;
	}

	public int getCourseId() {
		return this.courseId;
	}

	public void setCourseId(int courseId) {
		this.courseId = courseId;
	}

	public Date getStartTime() {
		return this.startTime;
	}

	public void setStartTime(Date startTime) {
		this.startTime = startTime;
	}

	public Date getEndTime() {
		return this.endTime;
	}

	public void setEndTime(Date endTime) {
		this.endTime = endTime;
	}

	public byte getStatus() {
		return this.status;
	}

	public void setStatus(byte status) {
		this.status = status;
	}

	public Double getWeight() {
		return this.weight;
	}

	public void setWeight(Double weight) {
		this.weight = weight;
	}

}
