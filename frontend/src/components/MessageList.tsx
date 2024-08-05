import React, { useEffect, useState } from 'react';
import { List, ListItem, ListItemText, Paper, TextField, Button, Box, Typography } from '@mui/material';
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

    useEffect(() => {
        const interval = setInterval(() => {
            fetchMessages(deviceType)
                .then(response => {
                    setMessages(response.data);
                })
                .catch(error => console.error('Error fetching messages:', error));
        }, 5000);

        return () => clearInterval(interval); // Cleanup interval on component unmount
    }, [deviceType]);

    const handleNewMessageChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        setNewMessage(event.target.value);
    };

    const handleSendMessage = () => {
        if (newMessage.trim() === '') return;

        createMessage(deviceType, newMessage)
            .then(response => {
                setMessages([response.data, ...messages]); // Add new message at the beginning
                setNewMessage('');
            })
            .catch(error => console.error('Error creating message:', error));
    };

    return (
        <Paper sx={{ padding: 2, height: '100%', display: 'flex', flexDirection: 'column' }}>
            <List sx={{ maxHeight: '80%', overflow: 'auto', flexGrow: 1 }}>
                {messages.slice().reverse().map((message, index) => (
                    <ListItem key={index}>
                        <ListItemText
                            primary={message.content}
                            secondary={
                                <Box mt={1}>
                                    <Typography variant="body2" color="textSecondary">
                                        {message.username} - {new Date(message.created_at).toLocaleString()}
                                    </Typography>
                                </Box>
                            }
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
                <Button onClick={handleSendMessage} variant="contained" color="primary" sx={{ ml: 2 }}>
                    Send
                </Button>
            </Box>
        </Paper>
    );
};

export default MessageList;
