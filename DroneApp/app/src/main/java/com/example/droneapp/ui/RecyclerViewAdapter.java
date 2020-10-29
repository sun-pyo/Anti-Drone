package com.example.droneapp.ui;

import android.content.Context;
import android.content.Intent;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ImageView;
import android.widget.TextView;
import android.widget.Toast;

import androidx.annotation.NonNull;
import androidx.recyclerview.widget.RecyclerView;

import com.example.droneapp.R;
import com.example.droneapp.db.entity.ProductsModel;
import com.example.droneapp.model.DateModel;
import com.example.droneapp.model.ListItem;

import org.w3c.dom.Text;

import java.text.SimpleDateFormat;
import java.util.Calendar;
import java.util.Date;
import java.util.List;
import java.util.Locale;

import static com.example.droneapp.model.ListItem.TYPE_PARENT;


interface OnItemDeleteListener {
    void onItemDeleteClicked(ProductsModel model);
}

public class RecyclerViewAdapter extends RecyclerView.Adapter<RecyclerView.ViewHolder> {

    private List<ListItem> listItemList;
    private OnItemDeleteListener onItemDeleteListener;
    //private Context mContext;

    /*
    public interface OnitemClickListener{
        void onitemClick(View v, int pos);
    }

    private OnitemClickListener mListener = null;

    public void setOnitemClickListener(OnitemClickListener listenr){
        this.mListener = listenr;
    }*/
    RecyclerViewAdapter(List<ListItem> listItemList, OnItemDeleteListener onItemDeleteListener) {
        this.listItemList = listItemList;
        this.onItemDeleteListener = onItemDeleteListener;
    }

    @NonNull
    @Override
    public RecyclerView.ViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
        if (viewType == TYPE_PARENT) {
            return new DateViewHolder(parent,LayoutInflater.from(parent.getContext()).inflate(R.layout.list_item_date, parent, false));
        } else {
            return new ProductsViewHolder(LayoutInflater.from(parent.getContext()).inflate(R.layout.list_item_single, parent, false), onItemDeleteListener);
        }
    }

    @Override
    public void onBindViewHolder(@NonNull RecyclerView.ViewHolder holder, int position) {
        ListItem item = listItemList.get(position);
        if(holder instanceof DateViewHolder){
            DateViewHolder dh = (DateViewHolder) holder;
            dh.bind(item);
        }else{
            ProductsViewHolder ph = (ProductsViewHolder) holder;
            ph.bind(item);
        }
    }



    @Override
    public int getItemViewType(int position) {
        return listItemList.get(position).getListItemType();
    }

    @Override
    public int getItemCount() {
        return listItemList.size();
    }


    static class ProductsViewHolder extends RecyclerView.ViewHolder {
        private TextView list_nod, list_distance, list_date,list_cam;
        private ImageView ivDelete;
        private OnItemDeleteListener onItemDeleteListener;

        public ProductsViewHolder(@NonNull View itemView, OnItemDeleteListener onItemDeleteListener) {
            super(itemView);
            list_cam = itemView.findViewById(R.id.list_cam);
            list_nod = itemView.findViewById(R.id.list_nod);
            list_distance = itemView.findViewById(R.id.list_distance);
            list_date = itemView.findViewById(R.id.list_date);
            ivDelete = itemView.findViewById(R.id.iv_delete);
            this.onItemDeleteListener = onItemDeleteListener;

        }

        void bind(ListItem item) {
            ProductsModel productsModel = (ProductsModel) item;
            list_cam.setText(String.valueOf(productsModel.getCaminfo()));
            list_nod.setText(String.valueOf(productsModel.getNumOfDrone()));
            list_distance.setText(String.valueOf(productsModel.getDistance()));
            list_date.setText(getFormatDateAndTimeString(productsModel.getDate()));
            ivDelete.setOnClickListener(view -> onItemDeleteListener.onItemDeleteClicked(productsModel));
            list_cam.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View v) {
                    String camNumber = String.valueOf(productsModel.getCaminfo()).replaceAll("[^0-9]","");
                    Toast.makeText(v.getContext(),camNumber,Toast.LENGTH_SHORT).show();
                    Intent intent = new Intent(v.getContext(),viewPage.class);
                    intent.putExtra("camNum",camNumber);
                    v.getContext().startActivity(intent);
                }
            });
        }

        private String getFormatDateAndTimeString(long seconds) {
            // 요일 정보를 가져오기 위한 포맷
            SimpleDateFormat dayFormat = new SimpleDateFormat("EEEE", Locale.KOREA);
            Calendar calendar = Calendar.getInstance(Locale.KOREA);
            calendar.setTime(new Date(seconds));
            return String.format("%d년 %02d월 %02d일 %02d시 %02d분",
                    calendar.get(Calendar.YEAR),
                    calendar.get(Calendar.MONTH) + 1,
                    calendar.get(Calendar.DAY_OF_MONTH),
                    calendar.get(Calendar.HOUR_OF_DAY),
                    calendar.get(Calendar.MINUTE)
            );
        }
    }

    static class DateViewHolder extends RecyclerView.ViewHolder {
        private TextView tvDate;

        public DateViewHolder(ViewGroup parent,@NonNull View itemView) {
            super(itemView);
            tvDate = itemView.findViewById(R.id.tv_date);
            tvDate.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View v) {
                    Toast.makeText(parent.getContext(),"asd",Toast.LENGTH_SHORT).show();

                }
            });

        }

        void bind(ListItem item) {
            DateModel date = (DateModel) item;
            tvDate.setText(date.getDateString());

        }

    }
}

