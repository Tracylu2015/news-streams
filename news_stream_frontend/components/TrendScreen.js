import React from 'react';
import { SafeAreaView } from 'react-native';
import TrendList from './TrendList';


function TrendScreen({ navigation }) {
    return (
        <SafeAreaView
            contentInsetAdjustmentBehavior="automatic">
            <TrendList navigation={navigation} />
        </SafeAreaView>
    );
}

export default TrendScreen;
