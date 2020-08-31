package com.example.droneapp.db.dao;

import androidx.room.Dao;
import androidx.room.Delete;
import androidx.room.Insert;
import androidx.room.Query;

import com.example.droneapp.db.entity.ProductsModel;

import java.util.List;

@Dao
public interface ProductsModelDao {
    @Insert
    long insert(ProductsModel productsModel);

    @Delete
    void delete(ProductsModel productsModel);

    @Query("SELECT * FROM products_model ORDER BY id desc")
    List<ProductsModel> getAll();

    @Query("SELECT date FROM products_model ORDER BY date desc")
    List<Long> getDates();
}
