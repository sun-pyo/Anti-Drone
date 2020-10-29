package com.example.droneapp.model;

import java.util.Objects;

public class DateModel implements ListItem{
    private String dateString;

    public DateModel(String dateString) {
        this.dateString = dateString;
    }

    public String getDateString() {
        return dateString;
    }

    public void setDateString(String dateString) {
        this.dateString = dateString;
    }

    @Override
    public int getListItemType() {
        return TYPE_PARENT;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;

        DateModel dateModel = (DateModel) o;
        return this.dateString.equals(dateModel.dateString);
    }

    @Override
    public int hashCode() {
        return Objects.hash(dateString);
    }
}
