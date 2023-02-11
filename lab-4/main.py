from forth import get_accuracy

accuracy = get_accuracy('test.csv', 'test_images', verbose=True, should_plot=False)
print('accuracy=%.3f' % accuracy)
