package com.example.demo.utils;

import javax.servlet.ServletOutputStream;
import javax.servlet.WriteListener;
import javax.servlet.http.HttpServletResponse;
import javax.servlet.http.HttpServletResponseWrapper;
import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.io.PrintWriter;

public class ResponseWrapper extends HttpServletResponseWrapper
{

    private ByteArrayOutputStream buffer= new ByteArrayOutputStream();

    private ServletOutputStream out= new WrapperOutputStream(buffer);

    private PrintWriter writer= new PrintWriter(buffer);

    public ResponseWrapper(HttpServletResponse httpServletResponse)
    {
        super(httpServletResponse);
    }

    @Override
    public ServletOutputStream getOutputStream()
    {
        return out;
    }

    @Override
    public void flushBuffer()
    {
        try
        {
            buffer.flush();
            buffer.close();
            writer.flush();
            writer.close();
        }
        catch (IOException e)
        {
            e.printStackTrace();
        }
    }

    @Override
    public PrintWriter getWriter(){
        return this.writer;
    }

    public byte[] getContent()
    {
        flushBuffer();
        return buffer.toByteArray();
    }




    class WrapperOutputStream extends ServletOutputStream
    {
        private ByteArrayOutputStream bos;

        private WrapperOutputStream(ByteArrayOutputStream bos)
        {
            this.bos = bos;
        }

        @Override
        public void write(int b)
        {
            bos.write(b);
        }

        @Override
        public boolean isReady() {
            return false;
        }

        @Override
        public void setWriteListener(WriteListener writeListener) {

        }
    }
}
