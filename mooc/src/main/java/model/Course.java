package model;
// Generated 2017-7-4 19:51:05 by Hibernate Tools 5.2.1.Final

/**
 * Course generated by hbm2java
 */
public class Course implements java.io.Serializable {

	private int id;
	private String name;
	private Integer teacherId;
	private String startTime;
	private String endTime;
	private Byte status;
	private String info;
	private String tp;
	private String place;
	private String score;
	private String teacher;
	private String people;

	public Course() {
	}

	public Course(int id) {
		this.id = id;
	}

	public Course(int id, String name, Integer teacherId, String startTime, String endTime, Byte status, String info,
			String tp, String place, String score, String teacher, String people) {
		this.id = id;
		this.name = name;
		this.teacherId = teacherId;
		this.startTime = startTime;
		this.endTime = endTime;
		this.status = status;
		this.info = info;
		this.tp = tp;
		this.place = place;
		this.score = score;
		this.teacher = teacher;
		this.people = people;
	}

	public int getId() {
		return this.id;
	}

	public void setId(int id) {
		this.id = id;
	}

	public String getName() {
		return this.name;
	}

	public void setName(String name) {
		this.name = name;
	}

	public Integer getTeacherId() {
		return this.teacherId;
	}

	public void setTeacherId(Integer teacherId) {
		this.teacherId = teacherId;
	}

	public String getStartTime() {
		return this.startTime;
	}

	public void setStartTime(String startTime) {
		this.startTime = startTime;
	}

	public String getEndTime() {
		return this.endTime;
	}

	public void setEndTime(String endTime) {
		this.endTime = endTime;
	}

	public Byte getStatus() {
		return this.status;
	}

	public void setStatus(Byte status) {
		this.status = status;
	}

	public String getInfo() {
		return this.info;
	}

	public void setInfo(String info) {
		this.info = info;
	}

	public String getTp() {
		return this.tp;
	}

	public void setTp(String tp) {
		this.tp = tp;
	}

	public String getPlace() {
		return this.place;
	}

	public void setPlace(String place) {
		this.place = place;
	}

	public String getScore() {
		return this.score;
	}

	public void setScore(String score) {
		this.score = score;
	}

	public String getTeacher() {
		return this.teacher;
	}

	public void setTeacher(String teacher) {
		this.teacher = teacher;
	}

	public String getPeople() {
		return this.people;
	}

	public void setPeople(String people) {
		this.people = people;
	}

}
