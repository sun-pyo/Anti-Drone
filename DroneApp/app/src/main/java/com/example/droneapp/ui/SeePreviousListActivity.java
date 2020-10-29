package com.example.droneapp.ui;

import android.os.Bundle;
import android.widget.ProgressBar;

import androidx.annotation.Nullable;
import androidx.appcompat.app.AppCompatActivity;
import androidx.recyclerview.widget.DividerItemDecoration;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;

import com.example.droneapp.R;
import com.example.droneapp.db.AppDatabase;
import com.example.droneapp.db.entity.ProductsModel;
import com.example.droneapp.model.DateModel;
import com.example.droneapp.model.ListItem;
import com.example.droneapp.util.AppExecutors;
import com.example.droneapp.util.DateUtils;

import java.util.ArrayList;
import java.util.Calendar;
import java.util.Date;
import java.util.List;
import java.util.Locale;

public class SeePreviousListActivity extends AppCompatActivity {
    private RecyclerViewAdapter mAdapter;
    private List<ListItem> listItemList;
    private AppExecutors appExecutors;
    private AppDatabase db;

    @Override
    protected void onCreate(@Nullable Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_see_prev_list);
        RecyclerView recyclerView = findViewById(R.id.recyclerView);
        listItemList = new ArrayList<>();


        mAdapter = new RecyclerViewAdapter(listItemList, this::deleteProductModel);
        appExecutors = new AppExecutors();
        db = AppDatabase.getDatabase(this);

        recyclerView.setHasFixedSize(true);

        LinearLayoutManager linearLayoutManager = new LinearLayoutManager(this);

        recyclerView.setLayoutManager(linearLayoutManager);
        DividerItemDecoration mDividerItemDecoration = new DividerItemDecoration(this,
                DividerItemDecoration.VERTICAL);
        recyclerView.addItemDecoration(mDividerItemDecoration);

        recyclerView.setAdapter(mAdapter);

        retrieveAllProductModelsFromDatabase();
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

    private void retrieveAllProductModelsFromDatabase() {
        appExecutors.diskIO().execute(() -> {
            List<Long> longValueList = db.getProductsModelDao().getDates();
            List<ProductsModel> productModelList = db.getProductsModelDao().getAll();
            for (long longValue : longValueList) {
                String dateString = DateUtils.getFormatDateAndTimeString(longValue);
                if (!this.listItemList.contains(new DateModel(dateString))) {
                    this.listItemList.add(new DateModel(dateString));

                    for (int i = 0; i < productModelList.size(); i++) {
                        Calendar calendar = Calendar.getInstance(Locale.KOREA);
                        calendar.setTime(new Date(longValue));
                        int year = calendar.get(Calendar.YEAR);
                        int month = calendar.get(Calendar.MONTH);
                        int day = calendar.get(Calendar.DAY_OF_MONTH);

                        calendar.setTime(new Date(productModelList.get(i).getDate()));
                        int pmYear = calendar.get(Calendar.YEAR);
                        int pmMonth = calendar.get(Calendar.MONTH);
                        int pmDay = calendar.get(Calendar.DAY_OF_MONTH);

                        if(year == pmYear && month == pmMonth && day==pmDay){
                            listItemList.add(productModelList.get(i));
                        }
                    }
                }
            }
            for (int i = 0; i < listItemList.size(); i++) {

            }
            appExecutors.mainThread().execute(() -> {
                mAdapter.notifyDataSetChanged();
            });
        });
    }

}
