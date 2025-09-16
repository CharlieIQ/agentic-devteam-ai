import React, { useState, useEffect } from 'react';
import ReactDOM from 'react-dom';
import './style.css';

function App() {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [posts, setPosts] = useState([]);
    const [content, setContent] = useState('');
    const [loggedIn, setLoggedIn] = useState(false);
    const backendUrl = 'http://localhost:8000'; 

    const handleRegister = async () => {
        try {
            const response = await fetch(`${backendUrl}/register`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username, password }),
            });
            if (!response.ok) throw new Error('Registration failed');
            alert('User registered!');
        } catch (error) {
            alert(error.message);
        }
    };

    const handleLogin = async () => {
        try {
            const response = await fetch(`${backendUrl}/login`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username, password }),
            });
            if (!response.ok) throw new Error('Login failed');
            setLoggedIn(true);
            alert('User logged in!');
            fetchPosts();
        } catch (error) {
            alert(error.message);
        }
    };

    const fetchPosts = async () => {
        const response = await fetch(`${backendUrl}/posts`);
        const data = await response.json();
        setPosts(data);
    };

    const handleCreatePost = async () => {
        try {
            const response = await fetch(`${backendUrl}/posts`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username, content }),
            });
            if (!response.ok) throw new Error('Post creation failed');
            alert('Post created!');
            fetchPosts();
            setContent('');
        } catch (error) {
            alert(error.message);
        }
    };

    return (
        <div className="App">
            <h1>Instagram Clone</h1>
            {!loggedIn ? (
                <div>
                    <h2>Register</h2>
                    <input type="text" placeholder="Username" value={username} onChange={e => setUsername(e.target.value)} />
                    <input type="password" placeholder="Password" value={password} onChange={e => setPassword(e.target.value)} />
                    <button onClick={handleRegister}>Register</button>

                    <h2>Login</h2>
                    <button onClick={handleLogin}>Login</button>
                </div>
            ) : (
                <div>
                    <h2>Create Post</h2>
                    <textarea placeholder="What's on your mind?" value={content} onChange={e => setContent(e.target.value)}></textarea>
                    <button onClick={handleCreatePost}>Post</button>
                    
                    <h2>Posts</h2>
                    {posts.map((post, index) => (
                        <div key={index}>
                            <h3>{post.author}</h3>
                            <p>{post.content}</p>
                            <h4>Comments:</h4>
                            {post.comments.map((comment, idx) => (
                                <p key={idx}><strong>{comment.author}</strong>: {comment.comment}</p>
                            ))}
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
}

ReactDOM.render(<App />, document.getElementById('root'));