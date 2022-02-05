import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { View, FlatList, StatusBar, StyleSheet, Text, Pressable } from "react-native";

const TrendList = ({ navigation }) => {
    const baseUrl = 'https://news-stream.spookyai.com';
    const [trends, setTrends] = useState([])

    useEffect(() => {
        const source = axios.CancelToken.source();
        const url = `${baseUrl}/api/trending`;
        const fetchTrends = async () => {
            try {
                const response = await axios.get(url, { cancelToken: source.token });
                // console.log(response.data);
                setTrends([...response.data])

            } catch (error) {
                if (axios.isCancel(error)) {
                    console.log('Data fetching cancelled');
                }
            }
        };
        fetchTrends();
        return () => source.cancel("Data fetching cancelled");
    }, []);


    const Item = ({ title }) => (
        <View style={styles.item}>
            <Text style={styles.title}>{title}</Text>
        </View>
    );


    const onPressNav = (item)=>{
        let tag = item.name
        console.log(item.name)
        navigation.navigate('Tweets', {tag})
    }
    const renderItem = ({ item }) => (
        <Pressable onPress={() => onPressNav(item)}>
            <View style={styles.item}>
                <Item title={item.name} />
                <View>
                    <Item title={item.count} style={styles.row} />
                </View>
            </View>
        </Pressable>
    );

    return (
        <FlatList
            data={trends}
            renderItem={renderItem}
            keyExtractor={item => item.name}
            onPress={onPressNav}
        />

    );
}

const styles = StyleSheet.create({
    container: {
        flex: 1,
        marginTop: StatusBar.currentHeight || 0,
    },

    item: {
        backgroundColor: '#aaaaaa',
        padding: 10,
        marginVertical: 6,
        marginHorizontal: 8,
        flex: 1,
        flexDirection: 'row',

    },
    row: {
        justifyContent: 'flex-end'
    },
    title: {
        fontSize: 24,
        color: '#111122'
    },
});



export default TrendList;
