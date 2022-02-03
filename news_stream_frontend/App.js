
import React from 'react';
import TrendList from './components/TrendList';
import Head from './components/Head';
import {
  SafeAreaView,
  ScrollView,
  StyleSheet,
  useColorScheme,

} from 'react-native';

import {
  Colors,

} from 'react-native/Libraries/NewAppScreen';


const App = () => {

  const isDarkMode = useColorScheme() === 'dark';

  const backgroundStyle = {
    backgroundColor: isDarkMode ? Colors.darker : Colors.lighter,
    flex: 1,
  };

  return (
    <SafeAreaView style={backgroundStyle}>
      {/* <StatusBar barStyle={isDarkMode ? 'light-content' : 'dark-content'} /> */}
      <Head />
      <SafeAreaView
        contentInsetAdjustmentBehavior="automatic"
        style={{marginBottom: 50}}>
        <TrendList />
      </SafeAreaView>
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({

});

export default App;
