package model;
// Generated 2017-7-4 19:51:05 by Hibernate Tools 5.2.1.Final

/**
 * Text generated by hbm2java
 */
public class Text implements java.io.Serializable {

	private int id;
	private byte[] content;

	public Text() {
	}

	public Text(int id) {
		this.id = id;
	}

	public Text(int id, byte[] content) {
		this.id = id;
		this.content = content;
	}

	public int getId() {
		return this.id;
	}

	public void setId(int id) {
		this.id = id;
	}

	public byte[] getContent() {
		return this.content;
	}

	public void setContent(byte[] content) {
		this.content = content;
	}

}