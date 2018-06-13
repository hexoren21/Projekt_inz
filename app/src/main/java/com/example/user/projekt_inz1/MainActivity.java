package com.example.user.projekt_inz1;

import android.bluetooth.BluetoothAdapter;
import android.bluetooth.BluetoothServerSocket;
import android.bluetooth.BluetoothSocket;
import android.content.Intent;
import android.os.CountDownTimer;
import android.os.Handler;
import android.os.Message;
import android.provider.Settings;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.TextView;

import com.firebase.client.Firebase;

import java.io.IOException;
import java.io.InputStream;
import java.text.DateFormat;
import java.text.SimpleDateFormat;
import java.util.Calendar;
import java.util.UUID;

public class MainActivity extends AppCompatActivity {
    Firebase myFirebase;
    TextView msg_box, status;
    public final String TAG = "MainActivity";
    BluetoothAdapter bluetoothAdapter;
    SendReceive sendReceive;
    BluetoothServerSocket serverSocket;
    static final int STATE_CONNECTING = 1;
    static final int STATE_CONNECTED = 2;
    static final int STATE_CONNECTION_LOST = 3;
    static final int STATE_MESSAGE_RECEIVED = 4;

    int REQUEST_ENABLE_BLUETOOTH = 1;

    private static final String bluetooth_server_name = "BTChat";
    private static final UUID bluetooth_UUID = UUID.fromString("8ce255c0-200a-11e0-ac64-0800200c9a66");


    @Override
    protected void onCreate(Bundle savedInstanceState)
    {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        findViewByIdeas();
        Firebase.setAndroidContext(this);
        String DeviceID = Settings.Secure.getString(getApplicationContext().getContentResolver(), Settings.Secure.ANDROID_ID);
        myFirebase = new Firebase("https://lokalizacja-gps.firebaseio.com/Users" + DeviceID);
        bluetoothAdapter=BluetoothAdapter.getDefaultAdapter();
        if(!bluetoothAdapter.isEnabled())
        {
            Intent enableIntent = new Intent(BluetoothAdapter.ACTION_REQUEST_ENABLE);
            startActivityForResult(enableIntent, REQUEST_ENABLE_BLUETOOTH);
        }
        ServerClass serverClass = new ServerClass();
        serverClass.start();
    }
    Handler handler = new Handler(new Handler.Callback()
    {
        @Override
        public boolean handleMessage(Message msg)
        {
            switch (msg.what)
            {
                case STATE_CONNECTING:
                    status.setText("Connecting");
                    break;
                case STATE_CONNECTED:
                    status.setText("Connected");
                    break;
                case STATE_CONNECTION_LOST:
                    status.setText("Connecting lost");
                    break;
                case STATE_MESSAGE_RECEIVED:
                    byte[] readBuff= (byte[]) msg.obj;
                    String tempMsg=new String(readBuff,0,msg.arg1);
                    send_to_server(tempMsg);
                    break;
            }
            return true;
        }
    });

    private void findViewByIdeas()
    {
        msg_box=(TextView) findViewById(R.id.msg);
        status=(TextView) findViewById(R.id.status);
    }

    private class ServerClass extends Thread
    {
        public ServerClass()
        {
            try
            {
                //utworzenie gniazda nasłuchujące od strony serwera
                serverSocket=bluetoothAdapter.listenUsingInsecureRfcommWithServiceRecord(bluetooth_server_name, bluetooth_UUID);
            } catch (IOException e)
            {
                e.printStackTrace();
            }
        }
        public void run()
        {
            BluetoothSocket socket=null;
            Log.e(TAG, " " + socket );
            while (socket == null)
            {
                try
                {
                    Message message = Message.obtain();
                    message.what = STATE_CONNECTING;
                    handler.sendMessage(message);
                    socket = serverSocket.accept();
                } catch (IOException e)
                {
                    e.printStackTrace();
                    Message message = Message.obtain();
                    message.what = STATE_CONNECTION_LOST;
                    handler.sendMessage(message);
                }
                if (socket != null)
                {
                    Message message = Message.obtain();
                    message.what = STATE_CONNECTED;
                    handler.sendMessage(message);
                    sendReceive=new SendReceive(socket);
                    sendReceive.start();
                    break;
                }
            }
        }
    }

    private class SendReceive extends Thread
    {
        private final BluetoothSocket bluetoothSocket;
        private final InputStream inputStream;
        public SendReceive (BluetoothSocket socket)
        {
            bluetoothSocket=socket;
            InputStream tempIn=null;
            try
            {
                tempIn = bluetoothSocket.getInputStream();
            }catch (IOException e)
            {
                e.printStackTrace();
            }
            inputStream=tempIn;
        }
        public void run()
        {
            byte[] buffer=new byte[1024];
            int bytes;
            while(true)
            {
                try
                {
                    //nowy strumien danych
                    bytes=inputStream.read(buffer);
                    handler.obtainMessage(STATE_MESSAGE_RECEIVED,bytes,-1,buffer).sendToTarget();
                }catch (IOException e)
                {
                    Log.e(TAG, "polaczenie zerwane " + e.getMessage() );
                    connectionLost();
                    break;
                }
            }
        }
        public void connectionLost()
        {
            // wysłij wiadomość do activity o połączeniu zerwanym
            Message message = Message.obtain();
            message.what = STATE_CONNECTION_LOST;
            handler.sendMessage(message);
            try
            {
                //zamkniecie interfejsu oraz serwera Bluetooth
                bluetoothSocket.close();
                serverSocket.close();
                ServerClass serverClass = new ServerClass();
                serverClass.start();
            } catch (IOException e)
            {
                e.printStackTrace();
            }
        }
    }
    public void send_to_server(String dane)
    {
        String[] coordinates = dane.split(",");
        msg_box.setText(coordinates[0] + "\n" + coordinates[1]);
        String myStringData = "Latitude: " + coordinates[0] +
                " Longitude: " + coordinates[1];

        DateFormat df = new SimpleDateFormat("yyyy-MM-dd 'at' HH:mm");
        final String date = df.format(Calendar.getInstance().getTime()).toString();
        Firebase myNewChild = myFirebase.child(date);
        myNewChild.setValue(myStringData);
        // zatrzymanie apki na 5 s
        new CountDownTimer(5, 1000)
        {
            public void onTick(long millisUntilFinished)
            {
            }
            public void onFinish()
            {
            }
        }.start();
    }
}
