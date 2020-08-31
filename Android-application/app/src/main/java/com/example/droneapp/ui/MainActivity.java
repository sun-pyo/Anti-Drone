package com.example.droneapp.ui;

import android.content.Intent;
import android.os.Bundle;
import android.util.Log;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.ProgressBar;
import android.widget.Toast;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;
import androidx.recyclerview.widget.DividerItemDecoration;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;

import com.example.droneapp.R;
import com.example.droneapp.db.AppDatabase;
import com.example.droneapp.db.entity.ProductsModel;
import com.example.droneapp.model.ListItem;
import com.example.droneapp.util.AppExecutors;
import com.google.android.gms.tasks.OnCompleteListener;
import com.google.android.gms.tasks.Task;
import com.google.firebase.Timestamp;
import com.google.firebase.firestore.DocumentReference;
import com.google.firebase.firestore.FirebaseFirestore;
import com.google.firebase.iid.FirebaseInstanceId;
import com.google.firebase.iid.InstanceIdResult;

import java.util.ArrayList;
import java.util.Calendar;
import java.util.Date;
import java.util.List;
import java.util.Locale;

public class MainActivity extends AppCompatActivity {
    private RecyclerViewAdapter mAdapter;
    private List<ListItem> listItemList;
    private ProgressBar progressBar;
    private AppExecutors appExecutors;
    private AppDatabase db;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        listItemList = new ArrayList<>();
        appExecutors = new AppExecutors();
        db = AppDatabase.getDatabase(this);

        FirebaseFirestore firebaseFirestore = FirebaseFirestore.getInstance();
        RecyclerView recyclerView = findViewById(R.id.firestore_list);
        progressBar = findViewById(R.id.progressBar);
        mAdapter = new RecyclerViewAdapter(listItemList, this::deleteProductModel);

        recyclerView.setHasFixedSize(true);

        LinearLayoutManager linearLayoutManager = new LinearLayoutManager(this);
        linearLayoutManager.setReverseLayout(true);
        linearLayoutManager.setStackFromEnd(true);

        recyclerView.setLayoutManager(linearLayoutManager);
        DividerItemDecoration mDividerItemDecoration = new DividerItemDecoration(this, DividerItemDecoration.VERTICAL);
        recyclerView.addItemDecoration(mDividerItemDecoration);

        recyclerView.setAdapter(mAdapter);


        DocumentReference docRef = firebaseFirestore.collection("robot").document("sky");
        docRef.update("Num_of_drone", 0);

        docRef.addSnapshotListener((documentSnapshot, e) -> {
            if (documentSnapshot == null) return;
            long numberOfDrones = (long) documentSnapshot.get("Num_of_drone");
            double distance;
            if (documentSnapshot.get("Distance") instanceof Long) {
                long temp = (long) documentSnapshot.get("Distance");
                distance = (double) temp;
            } else {
                distance = (double) documentSnapshot.get("Distance");
            }
            long date = ((Timestamp) documentSnapshot.get("date")).getSeconds() * 1000;
            ProductsModel model = new ProductsModel(numberOfDrones, distance, date);
            if (numberOfDrones >= 1) {
                if (listItemList.size() > 0) {
                    ProductsModel prevModel = (ProductsModel) listItemList.get(listItemList.size() - 1);

                    Calendar calendar = Calendar.getInstance(Locale.KOREA);
                    calendar.setTime(new Date(prevModel.getDate()));
                    int minute = calendar.get(Calendar.MINUTE);

                    calendar.setTime(new Date(model.getDate()));
                    int pmMinute = calendar.get(Calendar.MINUTE);

                    if (prevModel.getNumOfDrone() != model.getNumOfDrone()
                            && minute != pmMinute) {
                        listItemList.add(model);
                        mAdapter.notifyDataSetChanged();
                        progressBar.setVisibility(View.GONE);
                        putIntoDatabase(model);
                    }
                } else {
                    listItemList.add(model);
                    mAdapter.notifyDataSetChanged();
                    progressBar.setVisibility(View.GONE);
                    putIntoDatabase(model);
                }
            }
        });
    }




    private void deleteProductModel(ProductsModel productsModel) {
        appExecutors.diskIO().execute(() -> {
            db.getProductsModelDao().delete(productsModel);
            listItemList.remove(productsModel);
            appExecutors.mainThread().execute(() -> {
                mAdapter.notifyDataSetChanged();
            });
        });
    }

    private void putIntoDatabase(ProductsModel model) {
        appExecutors.diskIO().execute(() -> db.getProductsModelDao().insert(model));
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        getMenuInflater().inflate(R.menu.menu_prev_list, menu);
        return super.onCreateOptionsMenu(menu);
    }

    @Override
    public boolean onOptionsItemSelected(@NonNull MenuItem item) {
        if (item.getItemId() == R.id.action_list) {
            startActivity(new Intent(this, SeePreviousListActivity.class));
            return true;
        }
        return super.onOptionsItemSelected(item);
    }

}