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

    const ProfileItem = ({ item }) => (
        <View style={styles.item}>
            <Text style={styles.screenName}>{item}</Text>
        </View>
    );

    const renderItem = ({ item }) => (
        <View style={[styles.item, styles.elevation]}>
            <View style={styles.profile}>
                <Image style={styles.tinyLogo} source={item.user_info.profile_image_url == "" ? require("./images/t_icon.png") : { uri: item.user_info.profile_image_url }} />
                <View>
                    <ProfileItem item={item.user_info.screen_name} />
                </View>
                <View>
                    <Image style={styles.icon} source={item.user_info.verified === true ? require("./images/verified.png") : ""} />
                </View>
            </View>
            <View>
                <Item item={item.text} />
            </View>
            <View>
                <Image styles={styles.tImage} source={{ uri: item.media_url }} />
            </View>
            <View  >
                <Item item={new Date(item.created_at["$date"]).toUTCString()} />
            </View>

            <View style={styles.row} >
                <View style={styles.row}>
                    <Item item={item.user_info.followers_count} />
                    <Text style={styles.text}>
                        followers
                    </Text>
                </View >
                <View style={styles.row}>
                    <Item item={item.user_info.friends_count} />
                    <Text style={styles.text}>
                        friends
                    </Text>
                </View>
            </View>
        </View>
    );

    return (
        <FlatList
            data={tweet}
            renderItem={renderItem}
            keyExtractor={item => item.post_id}
        />
    );
};

const styles = StyleSheet.create({
    item: {
        backgroundColor: '#dedede',
        padding: 4,
        marginVertical: 10,
        marginHorizontal: 10,
        borderRadius: 8,
    },
    elevation: {
        elevation: 15,
        shadowColor: '#000022',
    },
    title: {
        fontSize: 16,
        color: '#000022'
    },
    row: {
        flex: 1,
        flexDirection: 'row',
        alignItems: 'center',
    },
    text: {
        fontSize: 16,
        color: '#000022',
    },
    tinyLogo: {
        width: 50,
        height: 50,
    },
    profile: {
        flex: 1,
        flexDirection: 'row',
        marginLeft: 16,
        paddingTop: 20,
        alignItems: 'center'
    },
    screenName: {
        fontWeight: 'bold',
        fontSize: 24,
        color: '#000022',
    },
    icon: {
        width: 20,
        height: 20,
    },
    tImage: {
        width: 100,
        height: 200,
    }
})

export default TagList;
