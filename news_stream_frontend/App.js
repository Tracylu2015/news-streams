
import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import TrendScreen from './components/TrendScreen';
import TweetScreen from './components/TweetScreen';



const Stack = createNativeStackNavigator();

const App = () => {

  return (
    <NavigationContainer>
      <Stack.Navigator>
        <Stack.Screen name="Home" component={TrendScreen} options={{
          title: 'Top Trending',
          headerStyle: {
            backgroundColor: '#f4511e',
          },
          headerTintColor: '#fff',
          headerTitleStyle: {
            fontWeight: 'bold', 
          },
          headerTitleAlign: 'center',
        }} />
        <Stack.Screen name="Tweets" component={TweetScreen} />
      </Stack.Navigator>
    </NavigationContainer >
  );
};


export default App;
