// Quick test to verify dummy data is working
import { getHomepage, getRecentArticles, getNavigation } from './src/lib/client.ts';

async function testDummyData() {
  try {
    console.log('Testing getHomepage...');
    const homepage = await getHomepage('en');
    console.log('Homepage data:', JSON.stringify(homepage, null, 2));

    console.log('\nTesting getRecentArticles...');
    const recentArticles = await getRecentArticles({ locale: 'en', first: 2 });
    console.log('Recent articles:', JSON.stringify(recentArticles, null, 2));

    console.log('\nTesting getNavigation...');
    const navigation = await getNavigation('en');
    console.log('Navigation data:', JSON.stringify(navigation, null, 2));

    console.log('\n✅ All dummy data functions working correctly!');
  } catch (error) {
    console.error('❌ Error testing dummy data:', error);
  }
}

testDummyData();
