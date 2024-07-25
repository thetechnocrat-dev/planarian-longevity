import React, { useEffect, useState } from 'react';
import { List, ListItem, ListItemText, Paper, TextField, Button, Box } from '@mui/material';
import { fetchMessages, createMessage } from '../api/messageApi';
import { Message } from '../types';

interface MessageListProps {
    deviceType: string;
}

const MessageList: React.FC<MessageListProps> = ({ deviceType }) => {
    const [messages, setMessages] = useState<Message[]>([]);
    const [newMessage, setNewMessage] = useState<string>('');

    useEffect(() => {
        if (deviceType) {
            fetchMessages(deviceType)
                .then(response => {
                    setMessages(response.data);
                })
                .catch(error => console.error('Error fetching messages:', error));
        }
    }, [deviceType]);

    const handleNewMessageChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        setNewMessage(event.target.value);
    };

    const handleSendMessage = () => {
        if (newMessage.trim() === '') return;

        createMessage(deviceType, newMessage)
            .then(response => {
                setMessages([...messages, response.data]);
                setNewMessage('');
            })
            .catch(error => console.error('Error creating message:', error));
    };

    return (
        <Paper style={{ padding: '20px', height: '100%' }}>
            <List style={{ maxHeight: '80%', overflow: 'auto' }}>
                {messages.map((message, index) => (
                    <ListItem key={index}>
                        <ListItemText
                            primary={`${message.username} - ${new Date(message.created_at).toLocaleString()}`}
                            secondary={message.content}
                        />
                    </ListItem>
                ))}
            </List>
            <Box display="flex" alignItems="center" mt={2}>
                <TextField
                    label="New Message"
                    value={newMessage}
                    onChange={handleNewMessageChange}
                    fullWidth
                />
                <Button onClick={handleSendMessage} variant="contained" color="primary" style={{ marginLeft: '10px' }}>
                    Send
                </Button>
            </Box>
        </Paper>
    );
};

export default MessageList;
