/* This file was generated by the ServiceGenerator.
 * The ServiceGenerator is Copyright (c) 2015 Google Inc.
 */

//
//  GTLSiftMainArticle.m
//

// ----------------------------------------------------------------------------
// NOTE: This file is generated from Google APIs Discovery Service.
// Service:
//   sift/v1
// Description:
//   API for sift
// Classes:
//   GTLSiftMainArticle (0 custom class methods, 8 custom properties)

#import "GTLSiftMainArticle.h"

// ----------------------------------------------------------------------------
//
//   GTLSiftMainArticle
//

@implementation GTLSiftMainArticle
@dynamic author, fullArticle, imageUrl, publication, published,
         publishedTimestamp, summarizedArticle, title;

+ (NSDictionary *)propertyToJSONKeyMap {
  NSDictionary *map =
    [NSDictionary dictionaryWithObjectsAndKeys:
      @"full_article", @"fullArticle",
      @"image_url", @"imageUrl",
      @"published_timestamp", @"publishedTimestamp",
      @"summarized_article", @"summarizedArticle",
      nil];
  return map;
}

@end
