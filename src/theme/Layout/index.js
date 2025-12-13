import React from 'react';
import Layout from '@theme-original/Layout';
import ChatbotWidget from '@site/src/components/ChatbotWidget';
import { AuthProvider } from '@site/src/contexts/AuthContext'; // Assuming you have this from previous work

export default function LayoutWrapper(props) {
  return (
    <>
      <AuthProvider>
        <Layout {...props}>
          {props.children}
          <ChatbotWidget />
        </Layout>
      </AuthProvider>
    </>
  );
}