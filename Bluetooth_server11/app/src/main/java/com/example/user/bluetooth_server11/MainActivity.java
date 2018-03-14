package com.example.user.bluetooth_server11;

import android.bluetooth.BluetoothAdapter;
import android.bluetooth.BluetoothDevice;
import android.bluetooth.BluetoothServerSocket;
import android.bluetooth.BluetoothSocket;
import android.content.Context;
import android.content.Intent;
import android.os.Handler;
import android.os.Message;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ListView;
import android.widget.TextView;

import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.util.Set;
import java.util.UUID;

public class MainActivity extends AppCompatActivity {
    Button listen;
    TextView msg_box, status;
    public final String TAG = "MainActivity";
    BluetoothAdapter bluetoothAdapter;

    SendReceive sendReceive;
    private BluetoothServerSocket serverSocket;
    //static final int STATE_LISTENING = 1;
    static final int STATE_CONNECTING = 2;
    static final int STATE_CONNECTED = 3;
    static final int STATE_CONNECTION_FAILED = 4;
    static final int STATE_MESSAGE_RECEIVED = 5;

    int REQUEST_ENABLE_BLUETOOTH = 1;

    private static final String APP_NAME = "BTChat";
    private static final UUID MY_UUID = UUID.fromString("8ce255c0-200a-11e0-ac64-0800200c9a66");
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        findViewByIdeas();
        bluetoothAdapter=BluetoothAdapter.getDefaultAdapter();
        if(!bluetoothAdapter.isEnabled()){
            Intent enableIntent = new Intent(BluetoothAdapter.ACTION_REQUEST_ENABLE);
            startActivityForResult(enableIntent, REQUEST_ENABLE_BLUETOOTH);
        }



       // implementListeners();

        ServerClass serverClass = new ServerClass();
        serverClass.start();
    }

    private void implementListeners() {
        listen.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                ServerClass serverClass = new ServerClass();
                serverClass.start();
            }
        });
    }

    Handler handler = new Handler(new Handler.Callback() {
        @Override
        public boolean handleMessage(Message msg) {
            switch (msg.what){
                case STATE_CONNECTING:
                    status.setText("Connecting");
                    break;
                case STATE_CONNECTED:
                    status.setText("Connected");
                    break;
                case STATE_CONNECTION_FAILED:
                    status.setText("Connecting Failed");
                    break;
                case STATE_MESSAGE_RECEIVED:
                    byte[] readBuff= (byte[]) msg.obj;
                    String tempMsg=new String(readBuff,0,msg.arg1);
                    msg_box.setText(tempMsg);
                    break;
            }
            return true;
        }
    });

    private void findViewByIdeas() {
        listen=(Button) findViewById(R.id.listen);
        msg_box=(TextView) findViewById(R.id.msg);
        status=(TextView) findViewById(R.id.status);

    }
    private class ServerClass extends Thread
    {
        //private BluetoothServerSocket serverSocket;
        public ServerClass(){
            try {
                serverSocket=bluetoothAdapter.listenUsingInsecureRfcommWithServiceRecord(APP_NAME, MY_UUID);
            } catch (IOException e) {
                e.printStackTrace();
            }
        }

        public void run()
        {
            BluetoothSocket socket=null;
            Log.e(TAG, "socket wynosi " + socket );


            while (socket == null) {
                try {
                    Message message = Message.obtain();
                    message.what = STATE_CONNECTING;
                    handler.sendMessage(message);
                    socket = serverSocket.accept();
                } catch (IOException e) {
                    e.printStackTrace();
                    Message message = Message.obtain();
                    message.what = STATE_CONNECTION_FAILED;
                    handler.sendMessage(message);
                }

                if (socket != null) {
                    Log.e(TAG, "socket jest rozny ");
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



    private class SendReceive extends Thread{
        private final BluetoothSocket bluetoothSocket;
        private final InputStream inputStream;

        public SendReceive (BluetoothSocket socket){
            bluetoothSocket=socket;
            InputStream tempIn=null;
            OutputStream tempOut=null;
            try {
                tempIn = bluetoothSocket.getInputStream();
                tempOut = bluetoothSocket.getOutputStream();
            }catch (IOException e){
                e.printStackTrace();
            }

            inputStream=tempIn;
        }
        public void run(){
            byte[] buffer=new byte[1024];
            int bytes;

            while(true){
                try {
                    bytes=inputStream.read(buffer);
                    handler.obtainMessage(STATE_MESSAGE_RECEIVED,bytes,-1,buffer).sendToTarget();
                }catch (IOException e){
                    Log.e(TAG, "write: Error writting to output stream. " + e.getMessage() );
                    connectionLost();
                    break;
                }
            }
        }
        private void connectionLost() {
            // Send a failure message back to the Activity
            Message message = Message.obtain();
            message.what = STATE_CONNECTION_FAILED;
            handler.sendMessage(message);
            try {
                bluetoothSocket.close();
                serverSocket.close();
                ServerClass serverClass = new ServerClass();
                serverClass.start();
            } catch (IOException e) {
                e.printStackTrace();
            }
        }

    }
}
