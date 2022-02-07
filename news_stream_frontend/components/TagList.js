import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { View, FlatList, StyleSheet, Text, Image, RefreshControl } from "react-native";



const TagList = ({ tag }) => {

    const [tweet, setTweet] = useState([])
    const baseUrl = 'https://news-stream.spookyai.com';
    const [refresh, setRefresh] = useState(false)
    const [onPull, setOnPull] = useState(false)

    useEffect(() => {
        const source = axios.CancelToken.source();
        const url = `${baseUrl}/api/tags/${tag}`;
        const fetchTrends = async () => {
            try {
                const response = await axios.get(url, { cancelToken: source.token });
                setRefresh(true)
                setTweet([...response.data])

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
    }, [tag, onPull]);

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


    const Time = (item) => {
        var now = new Date().getTime()
        var post_time = parseInt(item.created_at["$date"])
        var diff = Math.floor((now - post_time) / 1000)
        if (0 <= diff && diff < 60) {
            console.log(now, post_time, diff)
            return "posted just now";
        } else if (60 < diff && diff < 3600) {
            return "posted " + Math.floor(diff / 60) + " mins ago";
        } else if (3600 <= diff && diff < 86400) {
            return "posted " + Math.floor(diff / 3660) + " hours ago";
        } else {
            post_time = new Date(item.created_at["$date"]).toDateString()
            return post_time;
        }
    }


    const renderItem = ({ item }) => (
        <View style={[styles.item, styles.elevation]}>
            <View style={styles.profile}>
                <Image style={styles.tinyLogo} source={{ uri: item.user_info.profile_image_url }} />
                <View>
                    <ProfileItem item={item.user_info.screen_name} />
                </View>
                <View>
                    {item.user_info.verified === true ? <Image style={styles.icon} source={require("./images/verified.png")} /> : null}
                </View>
            </View>
            <View>
                <Item item={item.text} />
            </View>
            <View>
                {item.media_url !== "" ? <Image styles={styles.tImage} source={{ uri: item.media_url }} /> : null}
            </View>
            <View>
                <Text style={styles.text}>{Time(item)}</Text>
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
            refreshControl={
                <RefreshControl
                    refreshing={refresh}
                    onRefresh={() => setOnPull(true)}
                    colors={['#4a99e9']}
                />}
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
        marginLeft: 15,
    },
    tinyLogo: {
        width: 50,
        height: 50,
        borderRadius: 25,
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
        top: 2,
    },
    tImage: {
        width: 100,
        height: 100,
    }
})

export default TagList;
