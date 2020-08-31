package com.example.droneapp.db.entity;

import androidx.room.ColumnInfo;
import androidx.room.Entity;
import androidx.room.PrimaryKey;

import com.example.droneapp.model.ListItem;

@Entity(tableName = "products_model")
public class ProductsModel implements ListItem {
    @PrimaryKey(autoGenerate = true)
    @ColumnInfo(name = "id")
    private int id;
    @ColumnInfo(name = "numOfDrone")
    private long numOfDrone;
    @ColumnInfo(name = "distance")
    private double distance;
    @ColumnInfo(name = "date")
    private long date;

    public ProductsModel(long numOfDrone, double distance, long date) {
        this.numOfDrone = numOfDrone;
        this.distance = distance;
        this.date = date;
    }

    public void setId(int id) {
        this.id = id;
    }

    public int getId() {
        return id;
    }

    public long getNumOfDrone() {
        return numOfDrone;
    }

    public void setNumOfDrone(long numOfDrone) {
        this.numOfDrone = numOfDrone;
    }

    public double getDistance() {
        return distance;
    }

    public void setDistance(float distance) {
        this.distance = distance;
    }

    public long getDate() {
        return date;
    }

    public void setDate(long date) {
        this.date = date;
    }

    @Override
    public int getListItemType() {
        return TYPE_CHILD;
    }
}
