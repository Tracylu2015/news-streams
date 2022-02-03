import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { FlatList, StatusBar, StyleSheet, Text, TouchableOpacity } from "react-native";

const TrendList = () => {
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

    const [selectedName, setSelectedName] = useState("");

    const Item = ({ item, onPress, backgroundColor, textColor }) => (
        <TouchableOpacity onPress={onPress} style={[styles.item, backgroundColor]}>
            <Text style={[styles.title,  textColor]}>{item.name} </Text>
            <Text style={[styles.title,  textColor]}>{item.count} </Text>
        </TouchableOpacity>
    );

    const renderItem = ({ item }) => {
        const backgroundColor = item.name === selectedName ? "#6e3b6e" : "#f9c2ff";
        const color = item.name === selectedName ? 'white' : 'black';

        return (
            <Item
                item={item}
                onPress={() => setSelectedName(item.name)}
                backgroundColor={{ backgroundColor }}
                textColor={{ color }}
            />
        );
    };

    return (
        <FlatList
            data={trends}
            renderItem={renderItem}
            keyExtractor={(item) => item.name}
            extraData={selectedName}
        />
    );
};

const styles = StyleSheet.create({
    container: {
        flex: 1,
        marginTop: StatusBar.currentHeight || 0,
    },
    item: {
        padding: 20,
        marginVertical: 6,
        marginHorizontal: 8,
        flex: 1,
        flexDirection: "row",
        justifyContent:'space-between'
    },
    title: {
        fontSize: 22,
    },
});

export default TrendList;
