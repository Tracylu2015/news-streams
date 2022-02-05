import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { View, FlatList, StyleSheet, Text, Image } from "react-native";



const TagList = ({ tag }) => {

    const [tweet, setTweet] = useState([])
    const baseUrl = 'https://news-stream.spookyai.com';

    useEffect(() => {
        const source = axios.CancelToken.source();
        const url = `${baseUrl}/api/tags/${tag}`;
        const fetchTrends = async () => {
            try {
                const response = await axios.get(url, { cancelToken: source.token });
                setTweet([...response.data])

            } catch (error) {
                if (axios.isCancel(error)) {
                    console.log('Data fetching cancelled');
                }
            }
        };
        fetchTrends();
        return () => source.cancel("Data fetching cancelled");
    }, [tag]);

    const Item = ({ item }) => (
        <View style={styles.item}>
            <Text style={styles.title}>{item}</Text>
        </View>
    );

    const renderItem = ({ item }) => (
        <View style={styles.item}>
            <View style={styles.profile}>
                <Image style={styles.tinyLogo} source={{ uri: item.user_info.profile_image_url }} />
                <Item item={item.user_info.screen_name} />
            </View>
            <View>
                <Item item={item.user_info.create_at} />
            </View>
            <View>
                <Item item={item.text} />
            </View>
            <View style={styles.row} >
                <View style={styles.row}>
                    <Text style={styles.text}>
                        Favorite:
                    </Text>
                    <Item item={item.favorite_count} />
                </View >
                <View style={styles.row}>
                    <Text style={styles.text}>
                        Retweet:
                    </Text>
                    <Item item={item.retweet_count} />
                </View>
                <View style={styles.row}>
                    <Text style={styles.text}>
                        Reply:
                    </Text>
                    <Item item={item.reply_count} />
                </View>
            </View>
        </View>
    );

    return (
        <FlatList
            data={tweet}
            renderItem={renderItem}
            keyExtractor={item => item.post_id}
        // onPress={onPressNav}
        />
    );
};

const styles = StyleSheet.create({
    item: {
        backgroundColor: '#aaaaaa',
        padding: 4,
        marginVertical: 6,
        marginHorizontal: 8,
    },
    title: {
        fontSize: 16,
        color: '#000022'
    },
    row: {
        flex: 1,
        flexDirection: 'row',
    },
    text: {
        marginLeft: 15,
        fontSize: 16,
        color: '#000022'
    },
    tinyLogo: {
        width: 50,
        height: 50,
    },
    profile: {
        flex: 1,
        flexDirection: 'row',
        marginLeft:16,
        paddingTop: 20
    },
})

export default TagList;
