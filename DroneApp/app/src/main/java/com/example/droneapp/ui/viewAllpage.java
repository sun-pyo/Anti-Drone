package com.example.droneapp.ui;

import android.content.Intent;
import android.os.Bundle;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;

import androidx.appcompat.app.AppCompatActivity;

import com.example.droneapp.R;

public class viewAllpage extends AppCompatActivity {
    WebView cam1,cam2,cam3,cam4;
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.view_allpage);

        cam1 = (WebView)findViewById(R.id.cam1_view);
        cam2 = (WebView)findViewById(R.id.cam2_view);
        cam3 = (WebView)findViewById(R.id.cam3_view);
        cam4 = (WebView)findViewById(R.id.cam4_view);

        WebSettings cam1Setting = cam1.getSettings();
        WebSettings cam2Setting = cam2.getSettings();
        WebSettings cam3Setting = cam3.getSettings();
        WebSettings cam4Setting = cam4.getSettings();

        cam1Setting.setJavaScriptEnabled(true);
        cam2Setting.setJavaScriptEnabled(true);
        cam3Setting.setJavaScriptEnabled(true);
        cam4Setting.setJavaScriptEnabled(true);

        cam1Setting.setLoadWithOverviewMode(true);
        cam2Setting.setLoadWithOverviewMode(true);
        cam3Setting.setLoadWithOverviewMode(true);
        cam4Setting.setLoadWithOverviewMode(true);

        cam1Setting.setUseWideViewPort(true);
        cam2Setting.setUseWideViewPort(true);
        cam3Setting.setUseWideViewPort(true);
        cam4Setting.setUseWideViewPort(true);


        cam1.loadUrl("http://192.168.0.46:5000/video_feed/1");

        cam2.loadUrl("http://192.168.0.46:5000/video_feed/2");

        cam3.loadUrl("http://192.168.0.46:5000/video_feed/3");

        //cam4.getSettings().setJavaScriptEnabled(true);
        //cam4.setWebViewClient(new WebViewClient());
        cam4.loadUrl("http://192.168.0.46:5000/video_feed/4");

    }
}
