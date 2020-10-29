package com.example.droneapp.ui;

import android.content.Intent;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.os.AsyncTask;
import android.os.Bundle;
import android.os.Handler;
import android.os.Message;
import android.os.SystemClock;
import android.util.Log;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.widget.ImageView;
import android.widget.VideoView;

import androidx.appcompat.app.AppCompatActivity;

import com.example.droneapp.R;

import java.io.IOException;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.URI;
import java.net.URL;

public class viewPage extends AppCompatActivity {
    public static final int SEND_INFORMATION = 0;
    WebView camView;
    String camNum;

    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.view_page);

        Intent intent = getIntent();

        camNum = intent.getStringExtra("camNum");

        camView = (WebView) findViewById(R.id.cam_view);

        //camView.getSettings().setJavaScriptEnabled(true);
        //camView.setWebViewClient(new WebViewClient());
        camView.loadUrl("http://192.168.0.46:5000/video_feed/"+camNum);

    }
}

