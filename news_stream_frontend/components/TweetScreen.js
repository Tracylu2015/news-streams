import React from 'react';
import { SafeAreaView } from 'react-native';
import TagList from './TagList';

function TweetScreen({ navigation, route }) {

    const {tag} = route.params

    return (
        <SafeAreaView contentInsetAdjustmentBehavior="automatic">
            <TagList navigation={navigation} tag= {tag}/>
        </SafeAreaView>
    );
}
export default TweetScreen;
