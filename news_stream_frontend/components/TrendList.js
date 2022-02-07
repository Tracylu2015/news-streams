import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { View, FlatList, StatusBar, StyleSheet, Text, Pressable, RefreshControl } from "react-native";

const TrendList = ({ navigation }) => {
    const baseUrl = 'https://news-stream.spookyai.com';
    const [trends, setTrends] = useState([])
    const [refresh, setRefresh] = useState(false)
    const [onPull, setOnPull] = useState(false)

    useEffect(() => {
        const source = axios.CancelToken.source();
        const url = `${baseUrl}/api/trending`;
        const fetchTrends = async () => {
            try {
                const response = await axios.get(url, { cancelToken: source.token });
                setRefresh(true)
                setTrends([...response.data])
            } catch (error) {
                if (axios.isCancel(error)) {
                    console.log('Data fetching cancelled');
                }
            }
            finally {
                setRefresh(false)
            }
        };
        fetchTrends();
        return () => source.cancel("Data fetching cancelled");
    }, [onPull]);


    const Item = ({ title }) => (
        <View style={styles.item}>
            <Text style={styles.title}>{title}</Text>
        </View>
    );


    const onPressNav = (item) => {
        let tag = item.name
        navigation.navigate('Tweets', { tag })
    }
    const renderItem = ({ item }) => (
        <Pressable onPress={() => onPressNav(item)}>
            <View style={[styles.item, styles.elevation]}>
                <Item title={item.name} />
                <View>
                    <Item title={item.count} style={styles.row} />
                </View>
            </View>
        </Pressable>
    );


    return (
        <FlatList
            refreshControl={
                <RefreshControl
                    refreshing={refresh}
                    onRefresh={() => setOnPull(true)}
                    colors={['#4a99e9']}
                />}
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
        backgroundColor: '#ceeefe',
        padding: 10,
        marginVertical: 6,
        marginHorizontal: 8,
        flex: 1,
        flexDirection: 'row',
        borderRadius: 8
    },
    elevation: {
        elevation: 5,
        shadowColor: '#000022',
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
