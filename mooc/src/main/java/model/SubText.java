package model;
// Generated 2017-7-4 19:51:05 by Hibernate Tools 5.2.1.Final

/**
 * SubText generated by hbm2java
 */
public class SubText implements java.io.Serializable {

	private Integer id;
	private Integer taskId;
	private String textId;
	private Integer groupId;
	private String info;
	private String taskTitle;
	private String grade;
	private String comment;

	public SubText() {
	}

	public SubText(Integer taskId, String textId, Integer groupId, String info, String taskTitle, String grade,
			String comment) {
		this.taskId = taskId;
		this.textId = textId;
		this.groupId = groupId;
		this.info = info;
		this.taskTitle = taskTitle;
		this.grade = grade;
		this.comment = comment;
	}

	public Integer getId() {
		return this.id;
	}

	public void setId(Integer id) {
		this.id = id;
	}

	public Integer getTaskId() {
		return this.taskId;
	}

	public void setTaskId(Integer taskId) {
		this.taskId = taskId;
	}

	public String getTextId() {
		return this.textId;
	}

	public void setTextId(String textId) {
		this.textId = textId;
	}

	public Integer getGroupId() {
		return this.groupId;
	}

	public void setGroupId(Integer groupId) {
		this.groupId = groupId;
	}

	public String getInfo() {
		return this.info;
	}

	public void setInfo(String info) {
		this.info = info;
	}

	public String getTaskTitle() {
		return this.taskTitle;
	}

	public void setTaskTitle(String taskTitle) {
		this.taskTitle = taskTitle;
	}

	public String getGrade() {
		return this.grade;
	}

	public void setGrade(String grade) {
		this.grade = grade;
	}

	public String getComment() {
		return this.comment;
	}

	public void setComment(String comment) {
		this.comment = comment;
	}

}
