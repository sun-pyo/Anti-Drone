package com.example.droneapp.db;

import android.content.Context;

import androidx.room.Database;
import androidx.room.Room;
import androidx.room.RoomDatabase;

import com.example.droneapp.db.dao.ProductsModelDao;
import com.example.droneapp.db.entity.ProductsModel;

@Database(entities = {ProductsModel.class}, version = 1, exportSchema = false)
public abstract class AppDatabase extends RoomDatabase {
    public abstract ProductsModelDao getProductsModelDao();

    private static AppDatabase INSTANCE;

    public static AppDatabase getDatabase(final Context context) {
        if (INSTANCE == null) {
            synchronized (AppDatabase.class) {
                if (INSTANCE == null) {
                    INSTANCE = Room.databaseBuilder(context.getApplicationContext(),
                            AppDatabase.class, "drone.db")
                            .build();
                }
            }
        }
        return INSTANCE;
    }
}